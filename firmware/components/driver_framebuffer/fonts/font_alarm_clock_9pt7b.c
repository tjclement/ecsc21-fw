#include "../include/driver_framebuffer.h"
const uint8_t alarm_clock_9pt7bBitmaps[] = {
  0x00, 0xFA, 0x36, 0x80, 0x22, 0xBE, 0xCF, 0x52, 0x00, 0x7D, 0x28, 0xE2,
  0x9B, 0xC0, 0xCC, 0xEE, 0xDE, 0x60, 0x64, 0x4F, 0xA9, 0xF0, 0xC0, 0x72,
  0x09, 0x30, 0x64, 0x82, 0x70, 0xED, 0x7D, 0xC0, 0x49, 0x74, 0x80, 0x60,
  0xE0, 0x80, 0x24, 0x09, 0x00, 0x7C, 0x63, 0x08, 0xCB, 0xC0, 0xEC, 0x78,
  0x43, 0xE8, 0x43, 0xC0, 0x78, 0x42, 0xE0, 0x8B, 0xC0, 0x99, 0x9E, 0x12,
  0x20, 0x7C, 0x20, 0xE0, 0x8B, 0xC0, 0x44, 0x21, 0xE8, 0xCB, 0xC0, 0xF9,
  0x91, 0x12, 0x20, 0x7C, 0x63, 0xE8, 0xCB, 0xC0, 0x7C, 0x62, 0xE0, 0x8B,
  0xC0, 0x88, 0x8C, 0xCC, 0x70, 0x0F, 0xD8, 0xF1, 0x12, 0x04, 0x40, 0x78,
  0x43, 0xCA, 0xDB, 0xC0, 0x7C, 0x62, 0xE8, 0xCA, 0x40, 0x79, 0x4A, 0x22,
  0x9B, 0xC0, 0x7C, 0x21, 0x08, 0x43, 0xC0, 0x79, 0x4A, 0x02, 0x9B, 0xC0,
  0x7C, 0x21, 0xE8, 0x43, 0xC0, 0x7C, 0x20, 0xE8, 0x42, 0x00, 0x7C, 0x21,
  0x28, 0xCB, 0xC0, 0x4C, 0x62, 0xE8, 0xCA, 0x40, 0x79, 0x08, 0x02, 0x13,
  0xC0, 0x08, 0x43, 0x19, 0x4B, 0xC0, 0x09, 0x98, 0xEA, 0x90, 0x88, 0x08,
  0x88, 0xF0, 0x0E, 0x76, 0x08, 0x56, 0xC0, 0x0E, 0x72, 0x08, 0x56, 0x40,
  0x7C, 0x63, 0x08, 0xCB, 0xC0, 0x7C, 0x62, 0xE8, 0x42, 0x00, 0x7C, 0x63,
  0x0A, 0xCB, 0xC0, 0x7C, 0x62, 0xE8, 0x52, 0x40, 0x7C, 0x20, 0xE0, 0x8B,
  0xC0, 0xF4, 0x44, 0x04, 0x40, 0x8C, 0x43, 0x19, 0x4B, 0xC0, 0x36, 0x81,
  0x50, 0x05, 0x6B, 0x58, 0x76, 0x40, 0xB4, 0x0D, 0x40, 0x99, 0x9E, 0x44,
  0x78, 0x04, 0x04, 0x03, 0xC0, 0x72, 0x49, 0x30, 0xA0, 0x90, 0x64, 0x82,
  0xB0, 0x00, 0xF0, 0xC0, 0x78, 0x43, 0xE8, 0xCB, 0xC0, 0x44, 0x21, 0xE8,
  0xCB, 0xC0, 0xF8, 0x8F, 0x08, 0x43, 0xE8, 0xCB, 0xC0, 0x7C, 0x63, 0xE8,
  0x43, 0xC0, 0x7C, 0x20, 0xE8, 0x42, 0x00, 0x7C, 0x62, 0xE0, 0x8B, 0xC0,
  0x44, 0x20, 0xE8, 0xCA, 0x40, 0x68, 0xA0, 0x08, 0x43, 0x19, 0x4B, 0xC0,
  0x09, 0x98, 0xEA, 0x90, 0x88, 0x08, 0x88, 0xF0, 0xF5, 0x6C, 0x00, 0x74,
  0x65, 0x20, 0xF4, 0x65, 0xE0, 0x7C, 0x62, 0xE8, 0x42, 0x00, 0xF9, 0x9E,
  0x12, 0x20, 0x78, 0x88, 0x7C, 0x20, 0xE0, 0x8B, 0xC0, 0x48, 0x8F, 0x88,
  0xF0, 0x8C, 0xA5, 0xE0, 0x36, 0x81, 0x50, 0x85, 0x6D, 0xE0, 0xB4, 0x0D,
  0x40, 0x4C, 0x62, 0xE0, 0x8B, 0xC0, 0x78, 0x04, 0x04, 0x03, 0xC0, 0x34,
  0x4C, 0x44, 0x60, 0xFF, 0xC0, 0x62, 0x21, 0x22, 0xC0, 0x70 };

const GFXglyph alarm_clock_9pt7bGlyphs[] = {
  {     0,   1,   1,   6,    0,    0 },   // 0x20 ' '
  {     1,   1,   7,   3,    1,   -6 },   // 0x21 '!'
  {     2,   3,   3,   6,    2,   -6 },   // 0x22 '"'
  {     4,   5,   7,   7,    1,   -6 },   // 0x23 '#'
  {     9,   5,   7,   6,    0,   -6 },   // 0x24 '$'
  {    14,   4,   7,   6,    1,   -6 },   // 0x25 '%'
  {    18,   4,   7,   6,    0,   -6 },   // 0x26 '&'
  {    22,   1,   2,   6,    2,   -5 },   // 0x27 '''
  {    23,   3,   7,   6,    2,   -6 },   // 0x28 '('
  {    26,   3,   7,   6,    0,   -6 },   // 0x29 ')'
  {    29,   3,   6,   6,    1,   -6 },   // 0x2A '*'
  {    32,   3,   6,   6,    1,   -6 },   // 0x2B '+'
  {    35,   1,   3,   6,    1,   -3 },   // 0x2C ','
  {    36,   3,   1,   6,    1,   -3 },   // 0x2D '-'
  {    37,   1,   1,   3,    1,    0 },   // 0x2E '.'
  {    38,   3,   6,   6,    1,   -6 },   // 0x2F '/'
  {    41,   5,   7,   6,    0,   -6 },   // 0x30 '0'
  {    46,   1,   7,   6,    4,   -6 },   // 0x31 '1'
  {    47,   5,   7,   6,    0,   -6 },   // 0x32 '2'
  {    52,   5,   7,   6,    0,   -6 },   // 0x33 '3'
  {    57,   4,   7,   6,    1,   -6 },   // 0x34 '4'
  {    61,   5,   7,   6,    0,   -6 },   // 0x35 '5'
  {    66,   5,   7,   6,    0,   -6 },   // 0x36 '6'
  {    71,   4,   7,   6,    1,   -6 },   // 0x37 '7'
  {    75,   5,   7,   6,    0,   -6 },   // 0x38 '8'
  {    80,   5,   7,   6,    0,   -6 },   // 0x39 '9'
  {    85,   1,   5,   3,    1,   -4 },   // 0x3A ':'
  {    86,   1,   6,   3,    1,   -4 },   // 0x3B ';'
  {    87,   1,   6,   6,    3,   -6 },   // 0x3C '<'
  {    88,   4,   4,   6,    0,   -3 },   // 0x3D '='
  {    90,   1,   6,   6,    1,   -5 },   // 0x3E '>'
  {    91,   4,   7,   6,    1,   -6 },   // 0x3F '?'
  {    95,   5,   7,   6,    0,   -6 },   // 0x40 '@'
  {   100,   5,   7,   6,    0,   -6 },   // 0x41 'A'
  {   105,   5,   7,   6,    0,   -6 },   // 0x42 'B'
  {   110,   5,   7,   6,    0,   -6 },   // 0x43 'C'
  {   115,   5,   7,   6,    0,   -6 },   // 0x44 'D'
  {   120,   5,   7,   6,    0,   -6 },   // 0x45 'E'
  {   125,   5,   7,   6,    0,   -6 },   // 0x46 'F'
  {   130,   5,   7,   6,    0,   -6 },   // 0x47 'G'
  {   135,   5,   7,   6,    0,   -6 },   // 0x48 'H'
  {   140,   5,   7,   6,    0,   -6 },   // 0x49 'I'
  {   145,   5,   7,   6,    0,   -6 },   // 0x4A 'J'
  {   150,   4,   7,   6,    0,   -7 },   // 0x4B 'K'
  {   154,   4,   7,   6,    0,   -6 },   // 0x4C 'L'
  {   158,   5,   8,   6,    0,   -7 },   // 0x4D 'M'
  {   163,   5,   7,   6,    0,   -7 },   // 0x4E 'N'
  {   168,   5,   7,   6,    0,   -6 },   // 0x4F 'O'
  {   173,   5,   7,   6,    0,   -6 },   // 0x50 'P'
  {   178,   5,   7,   6,    0,   -6 },   // 0x51 'Q'
  {   183,   5,   7,   6,    0,   -6 },   // 0x52 'R'
  {   188,   5,   7,   6,    0,   -6 },   // 0x53 'S'
  {   193,   4,   7,   6,    1,   -6 },   // 0x54 'T'
  {   197,   5,   7,   6,    0,   -6 },   // 0x55 'U'
  {   202,   3,   7,   6,    2,   -7 },   // 0x56 'V'
  {   205,   5,   7,   6,    0,   -7 },   // 0x57 'W'
  {   210,   3,   6,   6,    1,   -6 },   // 0x58 'X'
  {   213,   4,   6,   6,    1,   -6 },   // 0x59 'Y'
  {   216,   5,   7,   6,    0,   -6 },   // 0x5A 'Z'
  {   221,   3,   7,   6,    0,   -6 },   // 0x5B '['
  {   224,   2,   6,   6,    2,   -6 },   // 0x5C '\'
  {   226,   3,   7,   6,    2,   -6 },   // 0x5D ']'
  {   229,   1,   1,   5,    0,    0 },   // 0x5E '^'
  {   230,   4,   1,   6,    0,    0 },   // 0x5F '_'
  {   231,   1,   2,   6,    1,   -5 },   // 0x60 '`'
  {   232,   5,   7,   6,    0,   -6 },   // 0x61 'a'
  {   237,   5,   7,   6,    0,   -6 },   // 0x62 'b'
  {   242,   4,   4,   6,    0,   -3 },   // 0x63 'c'
  {   244,   5,   7,   6,    0,   -6 },   // 0x64 'd'
  {   249,   5,   7,   6,    0,   -6 },   // 0x65 'e'
  {   254,   5,   7,   6,    0,   -6 },   // 0x66 'f'
  {   259,   5,   7,   6,    0,   -6 },   // 0x67 'g'
  {   264,   5,   7,   6,    0,   -6 },   // 0x68 'h'
  {   269,   2,   7,   6,    0,   -6 },   // 0x69 'i'
  {   271,   5,   7,   6,    0,   -6 },   // 0x6A 'j'
  {   276,   4,   7,   6,    0,   -7 },   // 0x6B 'k'
  {   280,   4,   7,   6,    0,   -6 },   // 0x6C 'l'
  {   284,   5,   4,   6,    0,   -3 },   // 0x6D 'm'
  {   287,   5,   4,   6,    0,   -3 },   // 0x6E 'n'
  {   290,   5,   4,   6,    0,   -3 },   // 0x6F 'o'
  {   293,   5,   7,   6,    0,   -6 },   // 0x70 'p'
  {   298,   4,   7,   6,    1,   -6 },   // 0x71 'q'
  {   302,   4,   4,   6,    0,   -3 },   // 0x72 'r'
  {   304,   5,   7,   6,    0,   -6 },   // 0x73 's'
  {   309,   4,   7,   6,    0,   -6 },   // 0x74 't'
  {   313,   5,   4,   6,    0,   -3 },   // 0x75 'u'
  {   316,   3,   7,   6,    2,   -7 },   // 0x76 'v'
  {   319,   5,   4,   6,    0,   -3 },   // 0x77 'w'
  {   322,   3,   6,   6,    1,   -6 },   // 0x78 'x'
  {   325,   5,   7,   6,    0,   -6 },   // 0x79 'y'
  {   330,   5,   7,   6,    0,   -6 },   // 0x7A 'z'
  {   335,   4,   7,   6,    1,   -6 },   // 0x7B '{'
  {   339,   1,  10,   5,    2,   -7 },   // 0x7C '|'
  {   341,   4,   7,   6,    0,   -6 },   // 0x7D '}'
  {   345,   5,   1,   5,    0,   -3 } }; // 0x7E '~'

const GFXfont alarm_clock_9pt7b = {
  (uint8_t  *)alarm_clock_9pt7bBitmaps,
  (GFXglyph *)alarm_clock_9pt7bGlyphs,
  0x20, 0x7E, 9 };//B

// Approx. 1018 bytes