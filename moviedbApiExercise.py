import json
import requests
from datetime import date,timedelta,datetime
import time
import os

filmCountRanges = range(0,960)

class films:
   
   api_key = 'e8a9d5f82d78ca210c8076d648685c12'
   
   def __init__(self):
      self.popularFilms = []
      self.totalFilms = []
      self.filmsInTheVision = []
      
      with open('total_films.json', 'r', encoding='UTF-8') as file:
         self.totalFilms = json.load(file)

         if self.totalFilms == [] or len(self.totalFilms) < len(filmCountRanges):
            self.totalFilms = []
            print('Films are updating now. Please wait.')
            for no in filmCountRanges:
               no = str(no)
               url = 'https://api.themoviedb.org/3/movie/'+no+'?api_key='
               response = requests.get(url+self.api_key)
               respText = response.text
               respDict = json.loads(respText)
               self.totalFilms.append(respDict)
               with open('total_films.json','w') as film_file:
                  json.dump(self.totalFilms, film_file)
            print('Films updated.')
      with open('total_films.json','r',encoding='UTF-8') as file:
         self.totalFilms = json.load(file)

   def findPopularFilms(self):

      for i in range(0,len(self.totalFilms)):
         try:
            if float(self.totalFilms[i]['popularity']) > 90:
               self.popularFilms.append(self.totalFilms[i]['original_title'])      
         except KeyError:
            continue
      
      for film in self.popularFilms:   
         print(film)

   def findFilmsViaKeyword(self,keyword):

      filmsViaKeyword = []

      for film in self.totalFilms:
         for a,b in film.items():
               try:
                  if isinstance(b, list):
                     for c in b :
                        for key,value in c.items():
                           try:
                              if keyword in value.lower():
                                 filmsViaKeyword.append(film['original_title'])
                              else:
                                 continue
                           except AttributeError:
                              continue   
                  else:
                     if keyword in b.lower():
                        filmsViaKeyword.append(film['original_title'])
                     else:
                        continue
               except AttributeError:
                  continue
      
      setFilms = set(filmsViaKeyword)  
      for film in setFilms:
         print(film)

   def findFilmsInTheVision(self):
   
      for film in self.totalFilms:
         try:
            releaseDate = film['release_date']
            releaseDate = releaseDate.split('-')

            day = int(releaseDate[2])
            month = int(releaseDate[1])
            year = int(releaseDate[0])

            filmReleaseDate = date(year,month,day)
            dateDelta = date.today() - filmReleaseDate

            if dateDelta.days < 60:
               self.filmsInTheVision.append(film['original_title'])
            else:
               continue
         except KeyError: 
            continue
      if self.filmsInTheVision == []:
         print("There aren't any movies on the show.")
      else:
         print (self.filmsInTheVision)

films = films()

while True:
   print('-------------------------------------------------------------------')
   secim = input("1- Popular films\n2- Find a film via keyword\n3- Find films in the show.\n4- Exit.\nChoose one: ")
   if secim == '4':
      break
   elif secim == '1' :
      films.findPopularFilms()
      time.sleep(2)
   elif secim == '2' :
      keyw = input ('Write the keyword in all lowercase letters: ') 
      films.findFilmsViaKeyword(keyw)
      time.sleep(2)
   elif secim == '3' :
      films.findFilmsInTheVision()
      time.sleep(2)