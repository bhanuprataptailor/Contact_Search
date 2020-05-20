from bs4 import BeautifulSoup
import time
import requests
# import datetime
import tldextract
import json
import csv
import os

sendgrid_key = '***'
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

def write_to_csv(di, fn):
    print('WRITING TO CSV\n', di, 'filename', fn)
    keys = di[0].keys()
    with open(fn, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(di)

def google_search(query, search_results):
    try:
        urls = []
        for j in search(query, tld="com", num=search_results, stop=search_results, pause=2):
            # print j
            urls.append(str(j))
        url_string = ', '.join(urls)
        return url_string
    except Exception as e:
        print (str(e))
        return ''

profiles_visited = []
searched_email_addresses = []

def check_email1(email_id):
    try:
        url = "https://api.sendgrid.com/v3/validations/email"

        payload = "{\n  \"email\": \"%s\",\n  \"source\": \"email send\"\n}" % email_id
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer "+sendgrid_key,
            'cache-control': "no-cache",
            'Postman-Token': "533e8b28-1c10-48a4-ad8a-71da3e4dcc27"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        # print(response.json())

        status = response.json().get('result').get('verdict')
        is_found = False
        if status == 'Valid':
            is_found = True
        # print email_id, status
        if status == 'Valid':
            return 'found'
        elif status == 'Invalid':
            return 'not_found'
        else:
            return 'may_be'
    except Exception as e:
        print(str(e))
        # print str(e)



def generate_emails(first_name, last_name, company):
    possible_domains = google_search(company, search_results=2).split(',')
    chosen_domain = None
    for domain in possible_domains:
        if domain.find('linkedin') == -1 and \
                domain.find('crunchbase') == -1 and \
                domain.find('glassdoor') == -1 and \
                domain.find('http') > -1:
            chosen_domain = tldextract.extract(domain).registered_domain.replace(',','')
    if chosen_domain:
        domain = chosen_domain.replace(',','')
    else:
        domain = company.replace(' ', '').replace('.', '').replace(',','') + '.com'
    first_name = first_name.lower().replace('.', '').replace(',','').replace('(','').replace(')','').replace(' ', '')
    last_name = last_name.lower().replace('.', '').replace(',','').replace('(','').replace(')','').replace(' ', '')
    domain = domain.lower()
    emails = [
        first_name + '.' + last_name + '@' + domain,
        first_name + last_name + '@' + domain,
        first_name + '@' + domain,
        first_name + '_' + last_name + '@' + domain,
        last_name + '@' + domain
    ]
    chosen_email = None
    for email in emails:
        print('searching email ', email)

        if email not in searched_email_addresses:
            status = check_email1(email_id=email)
            searched_email_addresses.append(email)
            print(status, '\n')
            if status == 'found':
                chosen_email = email
                found = True
                break
            else:
                found = False
    return found, chosen_email


def beautiful_soup_google_search(search_query, company):
    try:
        r = requests.get("https://www.google.com/search?q="+search_query)
        soup = BeautifulSoup(r.content, 'html5lib')
        # print r.content
        table = soup.findAll('div', {'class': 'kCrYT'})
        result = []
        for a in table:
            res = {}
            # print str(a),type(a), '\n'
            soup1 = BeautifulSoup(str(a))
            try:
                info_personal = str(soup1.findAll('div', {'class': 'BNeawe'})[0]).split('|')[0].split('>')[1]
            except Exception as e:
                print (str(e))
            try:
                Profile = str(soup1.find_all('a', href=True)[0]['href']).split('q=')[1].split('&')[0]
                res['First Name'] = info_personal.split('-')[0].split(' ')[0].lstrip().rstrip()
                res['Last Name'] = info_personal.split('-')[0].split(' ')[1].lstrip().rstrip()
                res['Position'] = info_personal.split('-')[1].lstrip().rstrip()
                res['Searched Company'] = info_personal.split('-')[2].replace('</div','').lstrip().rstrip()
                res['Profile'] = Profile.lstrip().rstrip()
                res['company'] = company
                 # print res,'\n\n'
                if Profile.lstrip().rstrip() not in profiles_visited:
                    result.append(res)
                    found, email = generate_emails(
                        first_name=res['First Name'],
                        last_name=res['Last Name'],
                        company=res['company'])
                    res['email'] = email
                    profiles_visited.append(Profile.lstrip().rstrip())
                    return res
            except Exception as e:
                print(str(e))
                # print(traceback.format_exc())
                # print str(e)
                pass
    except Exception as e:
        print(str(e))


def getting_final_result(job_results, titles):
    searched_companies = []
    checked_companies = []
    # job_results, titles = get_results()
    # job_results = job_results[count1:count2]
    Results = []
    for job_result in job_results:
        time.sleep(3)
        company = job_result.get('company')
        if company not in searched_companies:
            for title in titles:
                searched_companies.append(company)
                search_query = title+' '+company+' linkedin'
                print("searching for ", search_query)
                try:
                    Results.append(beautiful_soup_google_search(search_query=search_query, company=company))
                except Exception as e:
                    print('exception on getting beautiful google search', str(e))
                    pass
    for res in Results:
        try:
            if res['company'] not in checked_companies:
                for job_result in job_results:
                    if res['company'] == job_result['company']:
                        for a in job_result.keys():
                            res[a] = job_result[a]
                            checked_companies.append(res['company'])
        except Exception as e:
            print('company operation', str(e))
            pass

    return Results



print("--->Welcome to job_search\n")
searching = 1
while(searching):
    choice = int(input("---> How do yo wanna enter the data, \n1. copy paste in the specific format privide to you, "
                   "refer README.md \n2. Manually Enter the data. \n3. Any other number to exit.\n"))
    if choice == 1:
        inputs = input("--->Enter job_results\n")
        job_results = json.loads(inputs)
    elif choice == 2:
        enter_data = 1
        job_results = []
        companies = input("--->Enter the list of company names separated by comma (','), "
                          "example: amazon,google,microsoft \n").split(',')
        for company in companies:
            a = {}
            a["company"] = company
            job_results.append(a)
    else:
        break;

    enter = 1
    # titles = []
    titles = input("--->Enter the list of contact titles separated by comma (','), "
                      "example: hr,ceo,sales head \n").split(',')

    response = getting_final_result(job_results=job_results, titles=titles)
    print(response)
    fn = input("--->enter the file name for csv, example enter 'abc.csv'\n")
    currentDirectory = os.getcwd()
    print('--->saving location ', currentDirectory+'/'+fn, '\n')
    write_to_csv(di=response, fn=currentDirectory+'/'+fn)
