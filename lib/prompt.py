# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:49:35 2019

Standardisation module for command line prompting.

@author: jamesbriggs
"""


class go:
    def __init__(self, app,
                 version="0.0",
                 author="JBriggs",
                 email="",
                 detail=""):
        print("Py Tools\nThe following prompts will set up the " +
              app + " script.\nType \"help\""
              " at any point for more information on each parameter.")

        self.app = app
        self.version = version
        self.author = author
        self.email = email
        self.detail = detail

    def ask(self, question, detail="No help available."):
        # initialise answer to help
        answer = "help"
        # start the loop
        while answer.lower() == "help" or answer.lower() == "version":
            # ask user the question given
            answer = input(question+"\n>>> ")
            # if user answers 'help', respond with detail given
            if answer.lower() == "help":
                print(detail)
            elif answer.lower() == "version":
                print("{} v{}\nBuilt by {}\n{}\n{}".format(self.app,
                      self.version, self.author, self.email,
                      self.detail))
        # if user has given a valid answer, we return it
        return answer
