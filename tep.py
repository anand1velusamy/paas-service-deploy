import sys,time,httplib,json

job_id = 6511

conn = httplib.HTTPSConnection("testexecution.platform.intuit.com")

headers = {"Authorization": "Intuit_IAM_Authentication intuit_appid=Intuit.platform.servicesplatform.config, intuit_app_secret=prdFTmG81tCvqkwB3sYIvi1izi7zgyn9Pf7IK5Q0",
           "Cache-Control": "no-cache"}

conn.request("POST", "/v1/tester/jobs/%s/executions" % job_id, None, headers)
resp = json.loads(conn.getresponse().read())

c = 0
while c < 600:
    conn.request("GET", "/v1/tester/jobs/%s/executions/%s" % (job_id, resp.get('id')), None, headers)
    resp = json.loads(conn.getresponse().read())
    print resp.get('status')

    if resp.get('status') == "SUCCESS":
        sys.exit(0)
    time.sleep(2)
    c += 1

sys.exit(1)
