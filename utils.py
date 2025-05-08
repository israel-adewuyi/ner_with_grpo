ENTITY_EXAMPLES = {
    "Person": """
Example 1:
User: Soccer - Japan get lucky win , China in surprise defeat .
Assistant:
<think> 1. **Identify potential PERSON entities**: Look for names of people or family names, which are typically proper nouns (capitalized). 
- "Soccer" is a sport, not a person. - "Japan" and "China" are countries, not people. - "win" and "defeat" are events, not names. 
2. **Contextual clues**: - The sentence discusses teams (Japan, China) and outcomes, but no individual people are named. 
- No first or last names are mentioned. 
</think> <entity></entity>

Example 2:
User: China controlled most of the match and saw several chances missed until the 78th minute when Uzbek striker Igor Shkvyrin took advantage of a misdirected defensive header to lob the ball over the advancing Chinese keeper and into an empty net .
Assistant:
<think> 1. **Identify potential PERSON entities**: Look for names of people, which are typically proper nouns (capitalized) and could be first names, last names, or full names. 
- "China" is a country, not a person. - "Uzbek" is an adjective describing the striker, not a name. 
- "Igor Shkvyrin" is a full name (first name "Igor", last name "Shkvyrin"), so this is a PERSON. 
- "Chinese keeper" refers to a position (goalkeeper) and nationality, not a specific person's name. 
2. **Contextual clues**: - "Igor Shkvyrin" is explicitly mentioned as a striker, which is a role typically held by a person. 
- No other names or family names are mentioned in the sentence. 
</think> <entity>Igor Shkvyrin</entity>
""",
    "Location": """
Example 1:
User: Japan began the defence of their Asian Cup title with a lucky 2-1 win against Syria in a Group C championship match on Friday .
Assistant:
<think> 1. **Japan**: This is a country in East Asia, which is a politically and geographically defined location. It fits the criteria for a LOCATION entity. 
2. **Asian Cup**: This refers to a football tournament, not a specific geographic or political location, so it does not qualify as a LOCATION entity. 
3. **Syria**: This is a country in the Middle East, which is a politically and geographically defined location. It fits the criteria for a LOCATION entity. 
4. **Group C**: This refers to a group in the tournament, not a geographic or political location, so it does not qualify as a LOCATION entity. 
5. The rest of the words ("began", "the", "defence", "of", "their", "title", "with", "a", "lucky", "2-1", "win", "against", "in", "a", "championship", "match", "on", "Friday") are not location names and do not fit the criteria. 
</think> <entity>Japan, Syria</entity>

Example 2:
User: Oleg Shatskiku made sure of the win in injury time , hitting an unstoppable left foot shot from just outside the area .
Assistant: 
<think> 1. **Oleg Shatskiku**: This appears to be a person's name (likely a footballer) and not a location, so it does not qualify as a LOCATION entity. 
2. The rest of the words ("made", "sure", "of", "the", "win", "in", "injury", "time", "hitting", "an", "unstoppable", "left", "foot", "shot", "from", "just", "outside", "the", "area") do not refer to any geographic or political locations. 
3. **"the area"** could refer to a general space (e.g., penalty area in football), but it is not a specific named location, so it does not qualify as a LOCATION entity. </think> 
<entity></entity>
""",
    "Miscellaneous": """
Example 1:
User: Japan began the defence of their Asian Cup title with a lucky 2-1 win against Syria in a Group C championship match on Friday .
Assistant:
<think> 1. "Japan" - This is a country, which could be considered a nationality when referring to its people, but in this context, it's more of a geopolitical entity. Not a miscellaneous entity here. 
2. "Asian Cup" - This is an event (a football tournament), which falls under the miscellaneous category. 
3. "Syria" - Another country, similar to Japan, not a miscellaneous entity in this context. 
4. "Group C" - Part of the tournament structure, but not a miscellaneous entity by itself. 
5. "championship match" - Describes the type of event, but not a standalone miscellaneous entity. 
6. "Friday" - A day of the week, not a miscellaneous entity. 
</think> <entity>Asian Cup</entity>

Example 2:
User: Alpine SKIING-OFFICIALS hope to salvage world cup weekend .
Assistant:
<think> 1. **"Alpine SKIING"** - This refers to a sport (Alpine skiing), which could be considered a type of event or activity, but it's more of a general term. Not a specific miscellaneous entity here. 
2. **"OFFICIALS"** - Refers to people (organizers/referees), not a miscellaneous entity. 
3. **"world cup"** - This is a major sporting event (FIS Alpine Ski World Cup), which qualifies as a miscellaneous entity (event). 
4. **"weekend"** - A general time reference, not a miscellaneous entity. 
</think> <entity>world cup</entity>

Example 3:
User: Soccer - Japan get lucky win , China in surprise defeat .
Assistant:
<think> 1. **"Soccer"** - This is a sport, not a specific miscellaneous entity. 
2. **"Japan"** - A country, not a miscellaneous entity in this context. 
3. **"lucky win"** - A descriptive phrase, not a standalone entity. 
4. **"China"** - A country, not a miscellaneous entity here. 
5. **"surprise defeat"** - Another descriptive phrase, not an entity. 
</think> <entity></entity>
""",
    "Organization": """
Example 1:
User: Japan , co-hosts of the World Cup in 2002 and ranked 20th in the world by FIFA , are favourites to regain their title here .
Assistant: 
<think> 1. "Japan" - This could refer to the country, which is a governmental entity, but in this context, it's more about the national team, which is part of the Japan Football Association (an organization). 
However, "Japan" alone is typically considered a country (location), not an organization. 
2. "World Cup" - This is an event organized by FIFA, but it's not an organization itself. 
3. "FIFA" - This stands for Fédération Internationale de Football Association, which is the international governing body of football. It is clearly an organization. 
4. The rest of the words are either verbs, adjectives, or other parts of speech that do not refer to organizations. 
</think> <entity>FIFA</entity>

Example 2:
User: Soccer - Japan get lucky win , China in surprise defeat .
Assistant: 
<think> 1. "Soccer" - This is a sport, not an organization. 
2. "Japan" - Refers to the national team (Japan Football Association), but as before, "Japan" alone is typically a country (location). 
3. "China" - Similarly refers to the national team (Chinese Football Association), but "China" alone is a country (location). 
4. The rest of the words are verbs, adjectives, or other non-organization terms. 
</think> <entity></entity>
"""
}