# import textblob
from textblob import TextBlob

text1 = "Every day is a new opportunity to embrace joy and spread positivity. The world is full of amazing possibilities and beautiful moments waiting to be discovered. When you approach life with an open heart and a grateful mind, you’ll find that happiness and success naturally follow. Surround yourself with loving people, cherish each moment, and always believe in the best of what’s yet to come. The power of positivity can truly transform your life in the most wonderful ways."
text2 = "I hate everything and my dog died and my car won't start and I want to die."

sentiment = TextBlob(text2).sentiment
print(type(sentiment.polarity))