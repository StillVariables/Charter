# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests, json


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionBranchSearch(Action):

    def name(self) -> Text:
        return "action_branch_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("https://openapi.natwest.com/open-banking/v2.2/branches").json()

        try:
            entities = tracker.latest_message['entities']
            print("Last Message Now ", entities)
            TownName = None

            for e in entities:
                if e['entity'] == "TownName":
                    TownName = e['value']
            print(TownName)

            if TownName == None:
                dispatcher.utter_message("Sorry!! I'm still learning")

            for data in response["data"]:
                for br in data["Brand"]:
                    for bran in br["Branch"]:
                        pd_city = bran.get('PostalAddress').get('TownName')
                        if pd_city == TownName:
                            AddressLine = bran.get('PostalAddress').get('AddressLine')
                            cd = bran.get('PostalAddress').get('CountrySubDivision')
                            country = bran.get('PostalAddress').get('Country')
                            PostCode = bran.get('PostalAddress').get('PostCode')
                            contact = bran.get('ContactInfo')
                            lat = bran.get('PostalAddress').get('GeoLocation').get('GeographicCoordinates').get(
                                'Latitude')
                            long = bran.get('PostalAddress').get('GeoLocation').get('GeographicCoordinates').get(
                                'Longitude')
                            print(lat)
                            print(long)
                            dispatcher.utter_message(
                                "Address: " + str(AddressLine) + "\n" + "CountrySubDivison: " + str(
                                    cd) + "\n" + "Country: " + str(country) + "\n" + "PostCode: " + str(
                                    PostCode) + "\n" + "Contact: " + str(
                                    contact) + "\n" + "Map: " + "https://www.google.com/maps/place/" + lat + "," + long)

            print("Completed!!")

        except Exception as e:
            dispatcher.utter_message("Sorry!! I'm still learning")

        return []


class ActionAtmSearch(Action):

    def name(self) -> Text:
        return "action_atm_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("https://openapi.natwest.com/open-banking/v2.2/atms").json()
        try:
            entities = tracker.latest_message['entities']
            print("Last Message Now ", entities)
            CountrySubDivision = None

            for e in entities:
                if e['entity'] == "CountrySubDivision":
                    CountrySubDivision = e['value']

            print(CountrySubDivision)

            if CountrySubDivision == None:
                dispatcher.utter_message("Sorry!! I'm still learning")

            for data in response["data"]:
                for br in data["Brand"]:
                    for bran in br["ATM"]:
                        prsub = bran.get('Location').get('PostalAddress').get('CountrySubDivision')
                        if prsub[0] == CountrySubDivision:
                            AddressLine = bran.get('Location').get('PostalAddress').get('AddressLine')
                            # listToStr = ' '.join([('<a href="https://www.google.com/">' + str(elem) + '</a>') for elem in AddressLine])
                            listToStr = ' '.join([str(elem) for elem in AddressLine])
                            dispatcher.utter_message(listToStr)
                            # message1= (AddressLine[0]+" ,"+ AddressLine[1]+" ,"+ AddressLine[2]+" ," + AddressLine[3])
                            # print(type(message1))

            print("Completed!!")

        except Exception as e:
            dispatcher.utter_message("Sorry!! I'm still learning")


        return []


class ActionCCCSearch(Action):

    def name(self) -> Text:
        return "action_ccc_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("https://openapi.natwest.com/open-banking/v2.2/commercial-credit-cards").json()
        try:

            entities = tracker.latest_message['entities']
            print("Last Message Now ", entities)
            Name = None

            for e in entities:
                if e['entity'] == "Name":
                    Name = e['value']

            print(Name)
            # pdesc=None
            # pdurl=None
            # Notes=None
            if Name == None:
                dispatcher.utter_message("Sorry!! I'm still learning")

            for data in response["data"]:
                for br in data["Brand"]:
                    for bran in br["CCC"]:
                        if bran.get('Name') == Name:
                            for cms in bran["CCCMarketingState"]:
                                pdesc = cms.get('CoreProduct').get('ProductDescription')
                                pdurl = cms.get('CoreProduct').get('ProductURL')
                                Notes = cms.get('CoreProduct').get('Notes')

            dispatcher.utter_message(
                "Product Description: " + "\n" + str(pdesc) + "\n" + "\n" + "Product URL: " + "\n" + str(
                    pdurl) + "\n" + "Notes: " + "\n" + str(Notes))

            print("Completed!!")

        except Exception as e:
            dispatcher.utter_message("Sorry!! I'm still learning")

        return []


class ActionAccountDetails(Action):

    def name(self) -> Text:
        return "action_acc_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("http://localhost:3000/balance").json()

        for y in response["Balance"]:
            amount = y.get('Amount').get('Amount')
            date = y.get('DateTime')
            type = y.get('Type')
            dispatcher.utter_message("Type: " + str(type) + "\n" + "Amount: " + amount + "\n" + "Date: " + date)

        print("Completed!!")

        return []
