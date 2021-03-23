# Making sense of OSM tags

## dirt?
highway=footway, might be sidewalks?
surface="??"

### surface =
many possible values:
paved / unpaved / asphalt / concrete / paving_stones / sett / cobblestone / metal / wood / compacted / fine_gravel / gravel / pebblestone / plastic / grass_paver / grass / dirt / earth / mud / sand / ground


## bike ?

cycleway=<>
bicycle_road=yes
bicycle=use_sidepath
bicycle=??
bicycle=designated

highway=cycleway

tracktype = grade[1...5]

### some list
https://wiki.openstreetmap.org/wiki/Category:Cycleways
Cycleway/New Mapping Scheme
Key:bicycle road
Key:cyclestreet
Key:cycleway
Key:cycleway:both
Tag:cycleway:both=lane
Tag:cycleway:both=no
Key:cycleway:lane
Key:cycleway:left
Tag:cycleway:left=no
Tag:cycleway:left=track
Key:cycleway:right
Key:cycleway:right:oneway
Tag:cycleway:right=lane
Tag:cycleway:right=no
Tag:cycleway:right=track
Key:cycleway:surface
Tag:cycleway=asl
Tag:cycleway=bike box
Tag:cycleway=lane
Tag:cycleway=no
Ca:Tag:cycleway=opposite
Tag:cycleway=opposite
Tag:cycleway=opposite lane
Tag:cycleway=opposite track
Tag:cycleway=separate
Tag:cycleway=shared lane
Tag:cycleway=share busway
Tag:cycleway=sidepath
Tag:cycleway=track
User:Arcanma/Sandbox
User:Arcanma/Sandbox1
Tag:highway=cycleway
Tag:cycleway=proposed

### another link...?
https://wiki.openstreetmap.org/wiki/Tag:route%3Dbicycle


### cycleway tags from edmonton data
    <tag k="construction" v="cycleway"/>
    <tag k="cycleway" v="asl"/>
    <tag k="cycleway" v="crossing"/>
    <tag k="cycleway" v="lane"/>
    <tag k="cycleway" v="no"/>
    <tag k="cycleway" v="opposite"/>
    <tag k="cycleway" v="opposite_lane"/>
    <tag k="cycleway" v="share_busway"/>
    <tag k="cycleway" v="shared"/>
    <tag k="cycleway" v="shared_lane"/>
    <tag k="cycleway" v="track"/>
    <tag k="cycleway:left" v="lane"/>
    <tag k="cycleway:left" v="no"/>
    <tag k="cycleway:left" v="opposite_lane"/>
    <tag k="cycleway:left" v="opposite_track"/>
    <tag k="cycleway:left" v="share_busway"/>
    <tag k="cycleway:left" v="shared_lane"/>
    <tag k="cycleway:left" v="track"/>
    <tag k="cycleway:right" v="lane"/>
    <tag k="cycleway:right" v="opposite_lane"/>
    <tag k="cycleway:right" v="share_busway"/>
    <tag k="cycleway:right" v="shared_lane"/>
    <tag k="cycleway:right" v="track"/>
    <tag k="highway" v="cycleway"/>
