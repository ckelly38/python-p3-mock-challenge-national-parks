class NationalPark:

    def __init__(self, name):
        self.__ininit = True;
        self.setName(name);
        self.__ininit = False;
    
    def setName(self, val):
        if (type(val) == str and 2 < len(val)):
            if (self.__ininit): self._name = "" + val;
            else: raise Exception("name is not allowed to change!");
        else: raise Exception("name must be a string at least 3 characters long!");

    def getName(self): return self._name;

    name = property(getName, setName);

    def trips(self):
        return [tp for tp in Trip.all if tp.national_park == self];
    
    def all_visitors(self):
        return [tp.visitor for tp in self.trips()];

    def visitors(self):
        return list(set(self.all_visitors()));
    
    def total_visits(self):
        return len(self.trips());
    
    @classmethod
    def maxidx(cls, arr):
        maxval = max(arr);
        maxindxs = [i for i in range(len(arr)) if arr[i] == maxval];
        return maxindxs[0];

    def best_visitor(self):
        mvs = self.visitors();
        if (len(mvs) < 1): return None;
        elif (len(mvs) == 1): return mvs[0];
        else: return mvs[NationalPark.maxidx([vr.total_visits_at_park(self) for vr in mvs])];

    @classmethod
    def maxindx(cls, arr):
        maxval = max(arr);
        maxindxs = [i for i in range(len(arr)) if arr[i] == maxval];
        return maxindxs[0];

    @classmethod
    def most_visited(cls):
        #get the park with the most trips
        #need a list of all of the national parks and
        #then with how many trips each one of them has
        #we can do park.total_visits()
        #we need a list of all of the unique parks
        allparks = list(set([tp.national_park for tp in Trip.all]));
        if (len(allparks) < 1): return None;
        elif (len(allparks) == 1): return allparks[0];
        else: return allparks[cls.maxindx([p.total_visits() for p in allparks])];


class Trip:
    all = [];

    def __init__(self, visitor, national_park, start_date, end_date):
        self.setVisitor(visitor);
        self.setNationalPark(national_park);
        self.setStartDate(start_date);
        self.setEndDate(end_date);
        Trip.all.append(self);
    
    def setVisitor(self, val):
        if (type(val) == Visitor):
            self._visitor = val;
        else: raise Exception("vistor must be of type Visitor!");
    
    def getVisitor(self): return self._visitor;

    visitor = property(getVisitor, setVisitor);

    def setNationalPark(self, val):
        if (type(val) == NationalPark):
            self._national_park = val;
        else: raise Exception("national park must be of type NationalPark!");
    
    def getNationalPark(self): return self._national_park;

    national_park = property(getNationalPark, setNationalPark);

    def isValidDate(self, val):
        if (type(val) == str): pass;
        else: raise Exception("val must be a string!");
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                  "October", "November", "December"];
        endltrs = ["st", "nd", "rd", "th"];
        monthnm = "";
        monthi = -1;
        #print(val);
        for i in range(len(months)):
            try:
                if (val.index(months[i]) == 0):
                    monthnm = months[i];
                    monthi = i;
                    break;
            except(ValueError):
                pass;
        if (len(monthnm) < 1): return False;#no month found
        remstr = val[len(monthnm):];
        #print(remstr);
        if (remstr[0] == ' '): pass;
        else: return False;#no space
        remnumstr = remstr[1:-2];
        remendltrs = remstr[-2:];
        #print(remnumstr);
        #print(remendltrs);
        endi = -1;
        for i in range(len(endltrs)):
            if (endltrs[i] == remendltrs):
                endi = i;
                break;
        #print(endi);
        if (endi < 0 or len(endltrs) < endi or len(endltrs) == endi): return False;
        #endi is valid and end letters found
        mynum = int(remnumstr);
        if (monthi == 3 or monthi == 5 or monthi == 8 or monthi == 10): maxdays = 30;
        elif (monthi == 1): maxdays = 29;
        else: maxdays = 31;
        #print(maxdays);
        if (mynum < 1 or 31 < mynum): return False;
        elif (maxdays < mynum): return False;
        #1st, 2nd, 3rd, 4th ... 21st, 22nd, 23rd, 24th ... 31st
        eli = -1;
        if (mynum == 1 or mynum == 21 or mynum == 31): eli = 0;
        elif (mynum == 2 or mynum == 22): eli = 1;
        elif (mynum == 3 or mynum == 23): eli = 2;
        else: eli = 3;
        #print(eli);
        if (endi == eli): return True;
        else: return False;
    
    def setStartOrEndDate(self, val, usestart):
        if (self.isValidDate(val)):
            if (usestart): self._start_date = "" + val;
            else: self._end_date = "" + val;
        else: raise Exception("the date was invalid!");

    def getStartOrEndDate(self, usestart):
        if (usestart): return self._start_date;
        else: return self._end_date;

    def setStartDate(self, val): self.setStartOrEndDate(val, True);

    def setEndDate(self, val): self.setStartOrEndDate(val, False);

    def getStartDate(self): return self.getStartOrEndDate(True);

    def getEndDate(self): return self.getStartOrEndDate(False);

    start_date = property(getStartDate, setStartDate);

    end_date = property(getEndDate, setEndDate);


class Visitor:

    def __init__(self, name):
        self.setName(name);
    
    def setName(self, val):
        if (type(val) == str and 0 < len(val) and len(val) < 16):
            self._name = "" + val;
        else: raise Exception("name must be a string between 1 and 15 characters long (inclusive)!");

    def getName(self): return self._name;

    name = property(getName, setName);

    def trips(self):
        return [tp for tp in Trip.all if tp.visitor == self];
    
    def all_national_parks(self):
        return [tp.national_park for tp in self.trips()];

    def national_parks(self):
        return list(set(self.all_national_parks()));
    
    def total_visits_at_park(self, park):
        return len([1 for tp in self.trips() if tp.national_park == park]);
