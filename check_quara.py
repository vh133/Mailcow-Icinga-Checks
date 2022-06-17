#! /usr/bin/python3

#import modules
import sys, getopt, requests

#nagios return codes
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2
usage = 'usage: ./check_quara.py -w/--warn <integer> -c/--crit <integer> -a/--apiurl <string> -k/--apikey <string>'


# get commantline parameter
def command_line_validate(argv):
  try:
    opts, args = getopt.getopt(argv, 'w:c:a:k:', ['warn=', 'crit=', 'apiurl=', 'apikey='])
  except getopt.GetoptError:
    print(usage)
  try:
    for opt, arg in opts:
      if opt in ('-w', '--warn'):
        try:
          warn = int(arg)
        except:
          print('***warn value must be an integer***')
          sys.exit(CRITICAL)
      elif opt in ('-c', '--crit'):
        try:
          crit = int(arg)
        except:
          print('***crit value must be an integer***')
          sys.exit(CRITICAL)
      elif opt in ('-a', '--apiurl'):
        try:
          apiurl = str(arg)
        except:
          print('***apiurl value must be an string***')
          sys.exit(CRITICAL)
      elif opt in ('-k', '--apikey'):
        try:
          apikey = str(arg)
        except:
          print('***apikey value must be an string***')
          sys.exit(CRITICAL)
      else:
        print(usage)
    try:
      isinstance(warn, int)
    except:
      print('***warn level is required***')
      print(usage)
      sys.exit(CRITICAL)
    try:
      isinstance(crit, int)
    except:
      print('***crit level is required***')
      print(usage)
      sys.exit(CRITICAL)
    try:
      isinstance(apiurl, str)
    except:
      print('***apiurl is required***')
      print(usage)
      sys.exit(CRITICAL)
    try:
      isinstance(apikey, str)
    except:
      print('***apikey is required***')
      print(usage)
      sys.exit(CRITICAL)
  except:
    sys.exit(CRITICAL)
  # confirm that warning level is less than critical level, alert and exit if check fails
  if warn > crit:
    print('***warning level must be less than critical level***')
    sys.exit(CRITICAL)
  return warn, crit, apiurl, apikey


def check_quarantine(apiurl, apikey):
  try:
    ans = requests.get(url=apiurl, headers={'accept': 'application/json', 'X-API-Key': apikey})
    if ans.status_code != 200:
      print("UNKNOWN: sth went wrong. http status != 200")
      sys.exit(UNKNOWN)
    return len(ans.json())
  except:
    print('ERROR in check_quarantine')




# main function
def main():
  argv = sys.argv[1:]
  warn, crit, apiurl, apikey = command_line_validate(argv)
  counter = check_quarantine(apiurl, apikey)
  if counter >= crit:
    print('CRITICAL: ' + str(counter) + ' Mails in quarantine')
    sys.exit(CRITICAL)
  elif counter >= warn:
    print('WARNING: ' + str(counter) + ' Mails in quarantine')
    sys.exit(WARNING)
  elif counter < warn:
    print('OK: ' + str(counter) + ' Mails in quarantine')
    sys.exit(OK)
  else:
    print('UNKNOWN: sth went wrong... pls check script')
    sys.exit(UNKNOWN)

if __name__ == '__main__':
    main()