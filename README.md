**1. SETUP for Project**
**Extract scrapping module**
    
    a. INSTALL HOMEBREW
        $ ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
    
    b. INSTALL PYTHON
        $ brew install python
            
        OR
        https://www.python.org/downloads/ download from there, choose 2.7.15 or any latest version.
        
        OR Reference video
        https://www.youtube.com/watch?v=TgA4ObrowRg
        follow till step 4 only
    
    c. INSTALL PIP
        $ curl -O http://python-distribute.org/distribute_setup.py
        $ python distribute_setup.py
        $ curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
        $ python get-pip.py
        
        or
        
        $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        $ python get-pip.py

    d. Install requirement
        $ pip install -r requirements.txt

    e. run code
      Note: make sure you're at right directory,
        $ python3 contact_search.py
        or
        $ python contact_search.py



**If chosen copy paste in the specific format, 1.**

    data format: 
    list_of_dictionaries: example 
    [{"title": "Front Desk Receptionist - $21+ DOE", "url": "https://www.indeed.com/company/Protech-Systems-Group,-Inc./jobs/Front-Desk-Receptionist-6cb22a02c1250a4a?fccid=49a5f4efdc21e63d&vjs=3", "company": "ProTech Security Services", "summary": "Be able to handle high volume calls/emails and direct it to the right department.Keep track of employee's Guard Card expiration dates and contact employee to\u2026", "location": "San Francisco, CA (Financial District area)", "date": "22 days ago", "id": "4b04b96f-6821-4e26-b3a9-664b6aefffa7"}]


      
      



