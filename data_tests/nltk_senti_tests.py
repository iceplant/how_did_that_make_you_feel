from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

entries = ["Feeling a bit overwhelmed today. The work at Roblox has been intense, and I’m struggling to keep up with the pace. It’s one of those days where the pressure feels heavy, and I question if I’m really making a difference. On the flip side, I’m trying to remind myself of the progress I’ve made. I guess it’s all part of the journey, but today it feels particularly tough", 
"Today was a bit of a rollercoaster. I managed to overcome a challenging problem at work, which felt incredibly satisfying. The sense of achievement was a nice boost to my mood. Still, the day had its moments of frustration, and I’m learning to take the small victories as they come. It’s a mix of highs and lows, but I’m trying to stay focused on the positives.",
"I’m finding a sense of calm in the midst of a busy week. Despite the chaos of work, I felt a peaceful contentment when I took some time for myself. Reading and relaxing gave me a brief escape from the demands of daily life. There’s something comforting about these quiet moments, and they remind me of the balance I need to maintain.",
"Excitement is bubbling up as I prepare for my backpacking trip. I feel a mixture of anticipation and nervousness. The idea of disconnecting from everything and immersing myself in nature is exhilarating. I’m craving that solitude and the opportunity to reset. It’s moments like these that help me appreciate the balance between work and personal time.",
"'The beauty of the trail is overwhelming in the best way. There’s a profound sense of peace here, away from the city’s noise. Every step feels like a small victory, and the solitude is both calming and empowering. I’m reminded of why I love backpacking—it's a chance to reconnect with myself and appreciate the world’s simple beauty.",
"Returning from my trip, I’m filled with a mix of contentment and nostalgia. There’s something bittersweet about leaving the tranquility of nature behind. While I’m looking forward to being home, I also feel a sense of loss leaving the serenity of the outdoors. I’m grateful for the experiences and ready to carry this sense of calm into the week ahead."]

for sentence in entries:
  # print(sentence)
  ss = sid.polarity_scores(sentence)
  print(ss['compound'])
  # for k in sorted(ss):
  #   print('{0}: {1}, '.format(k, ss[k]), end='')
  # print()