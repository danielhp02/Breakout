# Breakout
A simple clone of Atari Breakout using Python 3 and Pygame

## Controls
|     Action       |       Key       |
| --------------   | --------------- |
| Move bat left    | Left Arrow Key  |
| Move bat right   | Right Arrow Key |
| Play ball        | Up Arrow Key    |
| Pause game       | Enter/Return    |
|Return Ball to bat| r               |
|Quit              | Escape          |

## Scoring
You get points for destroying bricks. Different coloured bricks are worth different amounts of points. The score earned for destroying each brick is shown in the table below.

|  Colour of Brick  | Points Scored |
| -------- | ------ |
| Red      | 7      |
| Orange   | 7      |
| Yellow   | 4      |
| Green    | 4      |
| Blue     | 1      |
| Cyan     | 1      |

## Lives
You lose a life when the ball falls past the bottom of the screen. The lives are in the form of extra balls. When you lose a life, you use one of the extra balls as a replacement for the one you just lost. Your current ball will appear as green/orange/red in the life display and will disappear once lost. The colour is dependent on how many balls you have left. All extra balls/lives will be grey.
