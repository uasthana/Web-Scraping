from bs4 import BeautifulSoup
import regex,urllib, urllib.request,os

try:
	file = open(os.path.expanduser(r"C:\Utkarsh\GIT\Python\WebScrapingTripAdvisor\UserDetails.csv"), "wb")
	file.write(b"Name" + b"," + b"Memberdescription" + b"," + b"Foodie" + b"," + b"PeaceandQuiet" + b"," + b"Excellent" + b"," + b"Average" + b","
               + b"Terrible" + b"\n")
except:
	os.remove(os.path.expanduser(r"C:\Utkarsh\GIT\Python\WebScrapingTripAdvisor\UserDetails.csv"))
	file = open(os.path.expanduser(r"C:\Utkarsh\Brookfield\TripAdvisorPython-master\UserDetails.csv"), "wb")
	file.write(b"Name" + b"," + b"Memberdescription" + b"," + b"Foodie" + b"," + b"PeaceandQuiet" + b"," + b"Excellent" + b"," + b"Average" + b","
               + b"Terrible" + b"\n")


#Scraping for UserId
NumberofUsers=200 #Select number of user data required
UserCounter=0
WebSites=["http://www.tripadvisor.ca/Hotel_Review-g147417-d507175-Reviews-Atlantis_Royal_Towers_Autograph_Collection-Paradise_Island_New_Providence_Island_Bahama.html#REVIEWS"]
for theurl in WebSites:
    thepage = urllib.request.urlopen(theurl)
    soup=BeautifulSoup(thepage, "html.parser")
    UserIdArray = []
    pattern = regex.compile(r"UID_(\w+)-CONT")
    while(UserCounter<NumberofUsers):
        x=0
        for user in soup.find_all(attrs={"class":"memberBadging g10n"}):
                id = soup.find_all("div",id=pattern)[x]["id"]
                uid=pattern.match(id).group(1)
                UserIdArray.append(uid)
                x=x+1
                UserCounter=UserCounter+1

        link=soup.find_all(attrs={"class":"nav next rndBtn ui_button primary taLnk"})
        if len(link)==0:
            break
        else:
            soup=BeautifulSoup(urllib.request.urlopen("http://www.tripadvisor.com" + link[0].get('href')))


#Scraping for user details using UserIdArray
usernamearray = []
memberdescriptionarray=[]
Foodiearray =  PeaceandQuietSeeker = Excellentarray = Averagearray= Terriblearray = ""
for id in UserIdArray:
    soup=BeautifulSoup(urllib.request.urlopen("http://www.tripadvisor.com/MemberOverlay?uid=" + id))
    x=0
    for member in soup.find_all(attrs={"class":"memberOverlay simple container moRedesign"}):
        membertag= member.text
        if membertag.find("Foodie")>0:
            if len(Foodiearray)==0:
                Foodiearray= ["1"]
            else:
                Foodiearray.append("1")
        elif membertag.find("Foodie")<0:
            if len(Foodiearray)==0:
                Foodiearray= ["0"]
            else:
                Foodiearray.append("0")
        if membertag.find("Peace and Quiet Seeker")>0:
            if len(PeaceandQuietSeeker)==0:
                PeaceandQuietSeeker= ["1"]
            else:
                PeaceandQuietSeeker.append("1")
        elif membertag.find("Peace and Quiet Seeker")<0:
            if len(PeaceandQuietSeeker)==0:
                PeaceandQuietSeeker= ["0"]
            else:
                PeaceandQuietSeeker.append("0")
    first_link = soup.find("span", string = "Excellent")
    if first_link is None:
        distribution = "0"
        if len(Excellentarray)==0:
            Excellentarray = [distribution]
        else:
            Excellentarray.append(distribution)
    else:
        distribution = first_link.find_next_siblings("span")[x].text
        if len(Excellentarray)==0:
            Excellentarray = [regex.sub(r'[^\w]','',distribution)]
        else:
            Excellentarray.append(regex.sub(r'[^\w]','',distribution))
    first_link = soup.find("span", string = "Average")
    if first_link is None:
        distribution = "0"
        if len(Averagearray)==0:
            Averagearray = [distribution]
        else:
            Averagearray.append(distribution)
    else:
        distribution = first_link.find_next_siblings("span")[x].text
        if len(Averagearray)==0:
            Averagearray = [regex.sub(r'[^\w]','',distribution)]
        else:
            Averagearray.append(regex.sub(r'[^\w]','',distribution))
    first_link = soup.find("span", string = "Terrible")
    if first_link is None:
        distribution = "0"
        if len(Terriblearray)==0:
            Terriblearray = [distribution]
        else:
            Terriblearray.append(distribution)
    else:
        distribution = first_link.find_next_siblings("span")[x].text
        if len(Terriblearray)==0:
            Terriblearray = [regex.sub(r'[^\w]','',distribution)]
        else:
            Terriblearray.append(regex.sub(r'[^\w]','',distribution))

    username = soup.findAll(attrs={"class":"username"})[x].text
    usernamearray.append(username)
    memberdescription = soup.findAll(attrs={"class":"memberdescription"})[x].text.replace("\n"," ").replace(","," ").strip()
    memberdescriptionarray.append(memberdescription)
    x=x+1

for x in range(0,len(UserIdArray)):
        Name=usernamearray[x]
        Memberdescription=memberdescriptionarray[x]
        Foodie=Foodiearray[x]
        PeaceandQuiet=PeaceandQuietSeeker[x]
        Excellent=Excellentarray[x]
        Average=Averagearray[x]
        Terrible=Terriblearray[x]

        file.write(bytes(Name, encoding="ascii",errors='ignore') +b"," + bytes(Memberdescription, encoding="ascii",errors='ignore') +b"," +
                   bytes(Foodie, encoding="ascii",errors='ignore') +b"," + bytes(PeaceandQuiet, encoding="ascii",errors='ignore') +b"," +
                   bytes(Excellent, encoding="ascii",errors='ignore') +b"," + bytes(Average, encoding="ascii",errors='ignore') +b"," +
                   bytes(Terrible, encoding="ascii",errors='ignore')  +b"\n" )


"""
print(Name)
print(Memberdescription)
print(Foodie)
print(PeaceandQuiet)
print(Excellent)
print(Average)
print(Terrible)
"""