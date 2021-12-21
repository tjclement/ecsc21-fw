import machine, system, flash, os

# Clear any flags from previous test cycles
from upysh import rm, mkdir
try:
    rm('/cache/system-flags.json')
except:
    pass

for dir in ['/private', '/private/system', '/proc']:
    try:
        mkdir(dir)
    except:
        pass


# Clear all CTF game state variables
machine.nvs_setint('system', 'splash_shown', 0)

# Write logo images
with open('/private/system/logo_small.png', 'wb') as file:
    file.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00<\x00\x00\x00<\x08\x06\x00\x00\x00:\xfc\xd9r\x00\x00\r,IDAThC\xe5\x9b\x0b\x90\x95\xc5\x95\xc7\x7f\xa7\xef\x8c@0\x12\x91\x91\x19\xccDP\x04\x120\xb8\x80\xc3Cd\x8d\x0f\xa2\x10t\r\x81\x90\xf2\x81\x06\xd6\x08\x02F\x89\x86L\xa5V\x14K\xb2\x9a\xa0\x99\x89\xe3\x03\x8d\x8fU#\x0bh\x12y\x18$\x86\x87\xc0\x0c\xc8#\x11\x05\x11\xc8dG\xb8\x03\x83(\t2\xc8p\xfb\xa4\xfa>\xe6~\xf7\xfd\xdd\x99qk\xab\xb6\xabn\xdd\xba\xdf\xd7}\xfa\xfc\xfb\x9c>}\x1e}\x85\xcf\xb9\xe9_\xf9RS!\xdd\x8d\tt\xb7h\xf7\x80\xe1lE\xbb\xbbi\x05\xa9\rY\xfef\x90ZkC\xb5\x85M\xd4J\x0f>\xf9<Y\x92\xcf\x83x\xd3~.F\xcc\xd5\x06\xc6(\xf4\xceg\x0e\x81w\xade\x91\x1a\xbb\xf4\x94\x126\xe53\xd6O\xdf6\x03|2\x18\xb8\n\xf4*\xc0}z\xfa\x99<W\x9f(\xf8\xd7\x11\xb3\xb2\xb0\xdb\xc9\xd7s\xf5\xf7\xf3\xbe\xd5\x80\xb5>\xf0\xad\x10\xf6\x16T\xc6\xf8\x99\xb0\xc5}D_\x0b`\x9e\x94\xe2\xd0\x92\x16\xd3\x08o\xa3\x16\xb6\xff5\xa0\xc9\xfc\xb5\x12x\xde\x80u\x0f\x9dB\x1d\xe4iD\xc6\xe6\\\xab\x13\xc0^E\x8e\x02\x9f\x02\xee\xfb\n\x90\xae\x91\x91\xfa\x11\xb0\x1c8\x15\xe8\x08\xea\xbe\xcf\x118%\'e7\xfa\x95\x80\xe8\x14)\xe6\xa0\x9f\xde\xb1>y\x01\xd6z\xce\t\xa9<\rrI\xd6I\xf6\x83\xa9Qd\x83\xa6v\x9b\xed@E\x1f\x7f\x08\x94\xa7v\xb1\x83\x04\x1d*P\x9a\x1d\x8a\xc0\x0eS`o\x94"\xde\xf6\x0b\xda7\xe0\x13A\xca\x0c\xa6&\x1ba\xf9\x8b"o\x83\xecL\x0346\xd0\x07\xe0XW\xed)\xe8 \xd0\x01\xd9\xd9\x0c\x18\x19+]C\xaf\xf8\x01\xed\x0b\xf0\x89`\xe0&\x83>\x93\x95`\x03\x04\x1e\xb3\x11\xb5\xcd\xd6\xf2\x00\x1cV\xfb\x8e`\xa7\x1883\x87\xb4\x85;\x02\xc5\xf6\x91\\\xa0s\x02\x0e\xed7\xb7\xaa\xf0X:B\xaf\xfdA\xb7\x8d\xf9\xa6\\\x10{g^Q\xa4:\x8bt]\xc7|\x01_(\xd8qq6\x7f\xb7\\\xb7\\s\x95\x0cH\x0fL\xbe[P\x12\xfa\xef\xacZ\x98\xede\xd3>\x86\x891\xeb\xd2\xf5Y\xf4\x9an\xb9e\xa6\xb6;\xbc\xcb\xf4m6\x08\xbb\x14\xf3T\xdb\x02\x0eM\x14\xe8\x1b\x07|F/\xbb\xbdb\xae\x1c\xb8n\xac\\\x96\x8e\xaf@\xc0\xf6\x923\xf9 \x13\xae\x8c\x12>\xb8\x9dS;\x9fav\x03Q\x9b\x1a\'\xf1\xc8|\xdd\xf0\xa3\xff\xd0\xa1\xee\xc9\xe2\'e\xd75c\xa4W\xb3\x94\xe7+\xf2A\x1b\xed\xe1\xb3\xc1\xdef\x9a\'^\xb1P\x8f\x8e\x9a\x11\xb6\xe5\xdcw\xb7,)\xbfC\xbe\x95\x0cL\x95\x0f\nJ\xec\xf9"|\x96\x0etF\xc0MAY"\xc8\xe8\xe4A?\x9e\xa3k~Q\xa5#b\xcf\x07\xf7\xe3\xcf\xeb\xde0\xfd\x9b\xa5\\\xad8\xd5\xce\xd8\xf2Pi\x1d%\xd8K\xe2,~w\xb4\xfd\xfb\xe2-\x9c\x16\xa3=\xe5&YZ97\x95G\x11~\x1d(\xb6\x93|\x03n\xdagf\x8b\xe1\x9e\xe4\x017L\xd3U\xbfY\xac)GR\xddzCI\x8fh\xef\xa3\x10x\xd8\xc2?2@\xf6\t\xd8\x19+\xbd\xc3\xa0Qx\xc1=P:\xdc\xa6\x10\x9dp\xad\xbc\xf9B\x95\\\x9a"i\xcb\xbd\x85gY7[BK\x91\xb0\x1e\xe4<\x1b2\xce\xf4t\xf6\xf6|\xec9\xad\x9e>K\x87\xa4\x831{\x9c\xf0\xd3\x8a8)\xb3T\x91\xd5\x19\xa4\xec\x17p\x92\xb1\xba\xff6ev\x06\xcd\xa9\xfc\x99TO\x99(\t\xbc\t\x1c6\x01;$y?\xa7\x00\x0e\xd5\x9bJU\xa6y\x81\x1dh\xa0\xe1\xdc\x0b\xed\x91\xe3\x9f\xa5\x0f\n\xce\xe9\x04\xbbv\xc6\xf7\x9a\xfc\r\xcc\xa3\xa9\xd2\x08\xd3\xf4\t8\xf4\x03\x81s\xe3\xec\xf5\xeac\xd9{$\xbd\xd6\xb4o\xc7\xee=\x9bL\xa7\xaeE\x14y{\x88\xf0\xab@\xb1\x9d\x9e\xf0\xcc\xfbC\x0f04d\xcd\xfad\xb2\xc3F\xdb5\x1b\xb7\xd0\xbco\xd3M\xbb\xe0\x1ea\xec\xad\x1e)g2^>\x00k\x92\xb1z\xa5J\x19?\'\xbb\xf5/\x1b\xc0\x9a\xf5KM\n\x8f\x01c\x87IW64\xdb\x18/\xf3\xa1z\xf3\x1bU&x\x9f=X\xa9\xeb\xca\x1f\xd0\x8b2[\xa1\xc8\x9b\x91\xe7\xc1\xb25\x1e)oQ\xcc\xcb-t-\xc7\n:8\xbex\xa3.\xb6\xacp\xe7E\x8e\xf6@\xb9\xac\xbb{\xba$\xf0*\xc2\xcb\x81b\xfb\xbd\x14\xc0M\xfb\x0b\xae\x14\xb1\xce\x95on\x07\x0fq\xf8\xec\x01\xf6\xd3\xa6\xa6\\^md\xc8{K\x0c\xbd\x06F\x87\x9f\x84\xc0\xdc$\xe3\xd5\x05t\xae@(\xda\xa7\x00\xe4\xc7\n.\x88\x88\xb6\xb0\xb1*7ha\xe4\xc1\xaeM\xf0\xb5\xab3l\x8f\xa4\x05(,\xa4\xee\x7f\xb6\x9a\x8eEg$\xda\x1f\x90Q\x05%\xa10\xb6\xe6el\xdag~.\x86\x99^\x1a?}@\xd7\xfe\xacR/\xce\xb5\xb2\xb1\xf7\xb7_\x01\xbfx>.\xe5\xb0\xf1\xda\xa9\xd8\xf3\x05\xfa\x0b\x9ar\xa2GFJ\x10d\x9b"\xef*\xb6\xb7\xa0c\xe2\xd2\x9dy\xbd\xe5\x97\x7f\xf4\xcb\x01\x94\xdf.\xd5\xf7\xcdJ4`@eA\x89\x9d\x91\x008\x144\xdb\x15\x9a\xbd&\xf7\xb2\xb4\xbf\xdd\x1c<HLf9g\xedX\x00G\xea\xe2\x80\t\x02\xa7\x03\xeds\x0e\x8dth\x04>\x06\xba\xc5\xfbw*\xb5|z\xd2\xe7x\xe0\xcb\xdd\xf8s\xed\xe6\xb8_\x10\x1d\xb9\xbb\xa0\xc4\x9e\xd7\x0c\xf8D\x90\x0b\rf\xa3\x97\xec\xee\xbd\xd4\xf5\xb9\xc8\xe6\x08\xd0R\x19y\xeav\xe1\xa6Y9]t_\x08\x9e\x9d\xabL\xae\xc8\xe1\xaa\xa6\xa1\xb4\xe3-S\x7f\xde\xb9\x14{_\xa9\xda\x11\x85\xddX\x1b\xe6,\x144\xf7h\xe4\xc0hn\x13\xa7\xeb\xaa\x17\x17\xa5:\x19\xb98\x1dT\x02\xd5[<R\x8e\r8\x0e\xf2\x8e"unc*8\x1c\xdd\x05=\'\x1a\xfeE\xf7\xac\x97\xfe\x90\x01\x96\xb7\x9d\x96\xe4\xd9n\xfe\x9el\x98?O\xc2\xaeo\xac)\xfc\xbc\xb0\xc4\xde\x15\x03\x9c\xa2\xce_\xecaw7\x1e\xcf?\x197\xaa7\xfc~U"`qA\xc5\xef5\x12\xe2\x9d\x05\xc4\xbc\xb2\xbf\x02\xfb@\x1bA\xaf1h\x82L\xe0\xea\x11\x96e\x19\xc3\x80\xcc\xab\xd0\xa1\x03\xbb\xff\xb1\xd7$$\x12\x05\xde\x0f\x94\xd8>R_O\xc7.j\x12\xa2\xd8\x8f\x8fp\xa4\xa8\x8f\xed\x94\xe7\xc2\x86\xbbo\xfc/\xc3\x80\xcb\xe3#e\x85bV*L\x01\x12\xd6\xdcC\xdd\x9d\x92\x8f\x81\xbd\\\xd0\x91\xf1\xed\xb0e\x99R6)\x7f\x95v\x94\x1bv\x9a#\xa7w"\x01\xc3!\xb1\xa7Jc\x90\xee\x85\x18\xb7\xd6\xcd\xadz\x0b\xef\x0f\x1fm\xf3\xca\'\xbb\xc1\xb7\\\x04U\x8b<g\xf1\x1e\xc5<\xa1\xf0\xbc\xcf\xa5\xbb\x11t\xbc\xe0R<\xb16\xf5\xdb\x96\'\x9b\xdd\x06\x9ft\x80\xb7\x96\x9a\xf7\x87\x0cH\xcc\x897a{H:\x83\xf5\xd4\x0bZs\xeb]:\xd8?\xf9H\xcf\xb5O\x1a\x86\xc6\x92\xb5\xf5\x10x\xca\xc2pHte\xb2P}\x19x3\x92\xe1\xd0\x92H\xbf\rK\xe0\xe2\x7f\xf7w\x0e{)?\xfe\x90\xd4L\xbe^\x120Xl\x99\x9c\x0c\x06F\x81.\xf5v\x9eQ\xae\xab\xab\x9e\xd1\x7f\xcd\x07p\xbb\x00\x1c\xdaa\xe8\xf0\xc5\xc8(\xd9\xa4\x98\xd7\x15\x1eM\xa2\xf2*\xb0:\xfa\xcc\xb9\xfb\t~\x1dp\'\xe8e\x82\x1d\x18\x91r\xe3Q\xe8\xd2\xc7\xf2Y\xccY\xf1\xc9\xd4\xd4\x9beu\xc5\x03\x92\x84AFK\xba|\xd5\xe5c\xed\xeaU\xeb\xc9\x0b\xf0\xc0b\xa8\xd9\xeaq:\x96)r@\xe1\'\x1e\x0e]V\xecOI\x1c\x97AB\xa82\x1fl\xbb\xc4\xbd<x\x80es\x9e\xd6\xfa\x92a\xac^\xb9\xd8$`\xb0\xc8\xcd\xd2\x144\xceT?\xe8e\xa3g\x99\xad\xa9\xad#/\x95\x9e<\x0c\x1e_\xec\x01\xfc\xbc"]\x15&z(\xdf\t\x1cJ\x02\xdc\x05\x98\xe7y\xb6\x16\xb4F\xb0\xd7\xc7\xf7\xf1\x0f\xc6Z\x9eN\ti\xb2\x8b\xba{)5\xbb7\x9a\x04\x0c\nw\xb7\x19\xe0[\x87\xc3\xaf\x16z\x00\xbf\xa0\xc8\xe9\n\xde\xbc\xc3]\xc0\x81$F\x9d\xbb\xf9\x90\xe7\xd9\x1fA\xb7\t\xf6\xba8\xe0\xdb\xc6[\x9eX\xebS\x97\xa3\xdd2\x02n+\x95\x1e\xd2\r\xde\xda\xec\xb1\xd0\xaf+\xa66\xc9\x9dy\x13x6\x89\xf1k\x01\xf7\x89\xb5y`\x8b\x05\xbd4\x0ex\xf8 K\xf5\xbe\xfc\x00gT\xe9\xb62Z\xed\x9d\xd1\xdaih\x1fN\xb1\x81l\x8d\xe6\xb6\xdcfq\xfet\xac9\xa3\x15\x93\x96\xf3\xd2\xaf\xf3\xbcs~\xf4O\xc0~[\xd0\xafG\x00\x1f\xff\x14\xba\xf4\xb6\x1co;\xa3\x95\xeaG\xb7\xc9\xb1\xd4\x04\xe6\xd7\x16\xf9z\x92\x04\xb3\t\xca-\xc6:\x08M3\xcd\x01G\x9b\x1fKm\xe9x\x8c\xbd\x00\x16,\xf7\xa8u=\x98y\x16\\`6(\x87J\xba\xeaP\x05\xd8\xc9\x82\xf6\x8a\xab\xf3\x84\x91\x96E\xef\xe4\xa7\xce\xaewF\xc7\xa3\xad]\xcb\x85\xf7\x0b\xd7N\xf2\xa4z\xdeP\xe4\r\x05W\x9fp\xea\x9b\x1c\x13;#\xf6"\xb0-\xd5\xb5|\xb5J\x19\x97#\xb5\x93i)2\xba\x96n@\xbaX\xf8\xb4s\xed\x8ec\xc7\xf8j\xbek\x9b\x9c\xd0\x0b\xef\xe7X\xf0\xf0w\x17dG?\xee\x85\x8b\x9c\xea@\xcfJ\x1f<dK\xdce\xe3\xabc\x07v\x1e\xd9k\xfax\xfb4\x07\x0f\xeea\xba<\xf4m\xb3t\xc5\x13\xcf\xe9\xc8|\x01\xff[_X\xb42Cx\xe8\xc2\xc2C\x91\x0c\x87\x0b\x0f\xd5\x9d\xc1]A\xfb\t\xa4\t\x0f\xbfs\x99\xe5\xb7\xef\xe5\xcb\x01L\x9b,k\x1e\x99#\t\t\xbd\x84\xf00\x9d?][G]\xcf\xb2\xfc\x13\x00+\x1e\x16.\x9d\xd06\t\x807_RF\xce\xcc?Z\xda\xb3\xd1\x04\xcf.%\xea\x8dG\x16,!\x01\x90I\xad{\x96\xd9\xb5\xb5u\xf8\xcei\xf5\xe9\x0c\xdb\xdf\xf5\x18-Wc2\xa0\x9e\xfcr6y\xc9n\x05K\x82\xd1\xea\xd7\xd7\xb2\xf3\xb0\x7f)\xf7\xec\xc1\x86\x9d\xebMr \x9a\x98\xe2\x89\xaauJ\x12o\xce<]u\xefC\xfe\xb3\x1e\x15\x93\x84\xa9\xf7{\x0c\xd6\x02E6+\xda\xc7\x9d\xab\xa0_\x91\x94:\xaf\x1c\x00\xa9S\xd8J\xb8\x08\xe7\x8a\xdf\xd6\xa3!U\xe5\xca\x8cg\xfcK\xf9\xbeY\xb2\xae\xfc\xf6\xc4Tm\xda$^\xba4\xed\xa1\xc3|Tz\x81=\xe67M{d\x87\xa1\xe3\x97\xa2\x8e\xc7Q0s\x9c\xb8\x92\xa43\x1b\xb4\x14\xc4\xadK\x01pc\xd2{\x01\xeb\xd2\xb4\xd1\xd0\xfd\xd8\'p\xdaW\xfd\x85\x87.M[\xb7\xcdt\xec\xd2\xd9G\x9a6\xac\xd6\xadH\xc4O\x1d\x01\x15\x0b<\xbe\xf4:E~\xd7\xc2D\xfc\x95\x89\xae\xe5\x8cq\x96\xaa\xb7r\xabu^\x89\xf8\xf0\xc6nE\xa9\xa5\xe6y\xc3\xc0+\xe2L\x99J\x1bI\xd8%7?\xa5\x96b\xb0w\xc6\x17o\xf3r\x18\xfc\xfd\xecRnQ\xa9%*\xe5\xbc\x8bi\xdf\xe8\x01o\xac\xf7\x1cE\x1f(\x81\xf9\xad\xab\x1e\xda\x9b\x04\xfdZ\xdc\x1e\\1\xd4\xf2\xa7\xda\xf4Rnq1-,\xe5\x16\x94K\x9f\x9b)\\\xf7\xa38s\xf2\xaab\xd2]Yr\x13\xf8\x90p\x98\x8f\xfe\x89!\xe2\x8b\xff\xa9L|$\xfd"\xb6\xaa\\\x9a\xc9\x11q\xcfo\x9c\xa6k^Z\x1c\xaf\xfe\xbbg\xa7\x048|\xecC\x13\xaf%\x7f\x0c\x01\xe7?\xa7\xbdp\x90\x07\xe0S\xc0\xfe\xd0\x80sN\xa2\xadk\x0f\xdb\xf4\xd1\xf1D\x17e\xc2\xb5\xb2\xea\x85\xaa\xd4{c\xea\xb7 \x1e#~2(\x0bA\xbe\x93\xacDw\xdd\xabo?\xfc\xb8\xbb=\x15i\xe3\xbf\xc9\xa6\x97\x9e5\x17\xc6~\xcbZ\xc5\xbc\xd66W\x1e\xecHA/\xf7\xd4\x99\xbeo?\xf9\xe5r\xa2\xe7\x00\xa4\xcf[\x85\x0bf\x8f\x06JlB\x8d\xbb\x99\xbfl\xb6/\x144\xef)\xa9\xfe\xf4s\x0bt\xfb\xa4\x1fj?7v\xdbJ\xf3a\xbf\xbe|9F\xc7<a\x91=Y\xa8\xfaT\xe9\xb0Z\x97\x82\x9d\x1e\xb7\r;6\xd2x\xfe5\xb6\x83{\xf7\xf8\x83R3\xf9\x86\xc4\xacddV]UP\xa2\xdf\xc8\xc4AV\x1fP\xf7\xd3%$\xa6!\xdd\xe0\xad\xefP7n\x92\xdd\xef\xcd\x1b\xc9\x0e\xc5\xe4r\x12\xf2\x00\xec\xe6\xb57\x08\xea\xaa\x8f\xd1\xd6\xb3\xccV\xbf<\xdft\x19\xd4?}U$P`O\x93\xa2\x8c7Lr\xdf\xa6=\xb1\x9fAFL\xda\x8b\xda\x8d\xc7\xf9\xacC{\xda5Kw\xb1"5m{O+|\xefr|\x1cp\xe3q\x1a;\xb4\',\xe5\xe4\x16(\xb0\xbd\xa5\x88]\xd9\xb4\xd6\x97\x97\xaf\x1fQ\x1a:a\x1c\xa1\xcc\x85Ow\xf5\xb0\xcaFn\xcdfkyJ\x98/@hj\xce\xab\x87M!\xb1\x03\xdb\x15\x933U\xe0\x0bpxg\xec\xe7\x0b!\x91\xc5 Wf\xdc\x1f;\x14\xd9\x16\xc9gely\x00vy-\xfb/$\xdc\xc4K\xa6+\xf0\x17\xd3\xce\x8e\x90\xced\xb8\xf2\x928\xc27\xe0\xd8\xb0\x93AS\x99\x94:O\xc5\xd6\x18\xad\xe8oT$9\xdb\x98\x03p\xb8\xc4\xe2\xae,\xb9\xfaR\xeeB\xfa\x82\x82\x12\x9b\\\xbb\xc8\xaa`y\x03v\xd4\\\xc2\xc0\x18\xa6\'\xdf\xe5J;\x93\xab\x0b\xbbl\xe4a\r\x7fk\x19H\xf4f\xac\xbb .\x1b@]V\xb3\xb3D\xbes\x83t\x86\xe7\xb0\xb5T\xa6\xbbx\x96cC\xe56Z\x99\x08\x84=2kf$\xdf\xe9\xca5ak\xdf\xbb\xbbW\xc6\xd8\x8al\x17H[m\xb4\xb2\x11p\x01\x87\xd50\xf0\xbcT+_\xe0\xee\xfa\x91\x11[\xe1\xbds\x95/\r\xd7\xbfE*\x9dn\xa2\xff7\x7f\xe3I\x07\xbe\xb5\x7f\xd4\x02\x16\x86\xb0\xcb\xfeO\xffQ+\x93z\xb9\xbcw\'\xa5(\x00E\x86@\x91\x853\x05\r\xdf\x89T\xa4\xc1\xc0AK\xa8!\x04\rG\x84\x86\xe2\xe2\x9c\'yK4\xb9y\xcc?\x01\x7f\x9cd\x004\xf5\xc4\xfd\x00\x00\x00\x00IEND\xaeB`\x82')
with open('/private/system/logo_med.png', 'wb') as file:
    file.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00x\x00\x00\x00x\x08\x06\x00\x00\x009d6\xd2\x00\x00\x1e?IDATx^\xdd]\t\x98T\xc5\xf1\xffU\xcf,\xc8\xa5\x80\x82;\x0b\x18<P\x10\x14A\xd4(\x8a\x18\x05\xa3(\x87G\x0eQ\xe3\x19\x89\x9a\xc4#\x82Q\xfc\x83D<\xc0\xa0\xd1\xe0\x11uE\x89\xc4x/\x8a\x11\x88\xca\xb2\xdc(\xe0\x02"\x87\x80\xb2\xbb\xb3\xc8%\xc2\x82\xb0;]\xff\xaffg`vw\xde\xeb~3o\x86%\xf5}\xf3\xe9\xf2\xba\xab\xab\xeb\xf7\xaa_\x1fU\xd5\x84\xff!\xe20ZU\x01\x9d\x15\xd4\x89\x9a\xd1F)4f\xa0\t4\x9a@q\xe3\xea\xff\x02\xd0\xd8\x05\xd0.\x00\xbbH\xa1"\xfa7a\x8bf\xb5\xacRW-k\xdc\x16%\xff+j\xa1\x83\xb5#\xbc\x05m#{\x02\xe7\x81\xf8\xa7\x00\x9f\x08Pg\x00\xad\xfc\xe8\x0f\x01\xdb\x18\xb4\x0c\xe0e`\x9a\x1bh\x18\xf9\x94\x0e?8A?h\x00\x8e\x02\xba7p&3\x9f\t\xc2\xf9\x04\x9c\xec\x07\x98\xb6<\x18(\x06\xe3c"\x9a\x1bh\x10\x99{\xb0\x00^\xaf\x01\xfe\xa1\x0cG4V\x81\xfe\xccz\x00\x81\xfa\xdb\x82\x91\x8dr\x0c\x9eL\xa4\nv\xe9\xc8\xe4C\xf3\xb09\x1bm\xa6\xd2F\xbd\x04\x98\xcb\x03\xfd#\xcc\x03\x08\xe8\xcf\xc0\x11\xa9t,[u\x08\xd8\xcc\xc0\xe4\x00Q\x01\xe5F&g\xab]\xdbv\xea\x15\xc0Ue\xea\xb7 \xfc\x16\xc0\xa9\xb6\x1d\xa8O\xe5\x08X\x0c _\xb1\xce\xa7<\x99\xc8\x1dx\xaa\x17\x00\x1f\xec\xc0\xd6\x86\x91\x19+A\xc8\xdf\xcd:\xff@\x0f\xdf\x07\x14\xe0\xaa\xf2\xc0\r`\xbe\xf5`\xb5X\xa3}260#?\x98\xa7G\x13\xa1\xd2X>\x03\x05\x0e\x08\xc0\x95\xa5\xe8\tEC\xeb\xdb\xc4)\x03\xfa\x8d\xb1\xa4y\x01\xc2h\xca\x8d|\x90\xb96\x92s\xce*\xc02+nB\xea\x1e\x06\x86f\xbb\xa3\xf5\xa4\xbd\xf1\x81\xa0\x1eM\xad\x10\xce\x96<Y\x03\xb8\xaa,p5\x83\x87\x13\xe1\x84\x8cu\xae\x02\xa0r\x06\xbe\x03\xb0\x15\x80\xfc}\x06\x80\xee\x8c\xe8\x0e\x96\x02\xa4\xc3\xac\xa3\xbbY\xa05\x04\xfe\x08@S\x80\x0f\x05\x90+?\x02\x1f\x961\tA\x845\xaciT0/21s\xad\xec\xe7\x9c\x15\x80+\xcb\x94|\x83\xee\xf3\xb5C{\x01\xfa\x92A\xeb\x00|\xc7\xa0\xf2j@\xeb\xd0o\x00\x9c\xef\xd0\xf2\x12\x00\xe3\xea>\xe3F\t`\x1f-\xfbd\x044\xf0Uz\x01\xfa\tU\xa2\x87Q\x8f\xcc~\x9b3\n\xf0\xee2\xfc$\x87h\x1c@\x97\xf9\xa2\x9e\xad\x00\xad`\xd0W\x00\xadd;\x96)\x00\x9c\x8c1\x9f@\xe0\x8e\x00w"\xa0\xa5]\xd3\xe6R<C\x83\x875\x08a\x81\xb9lj%2\x060o\x0c^\xa8\xb5~\x82\x81N\xa9\x89\x960\xcc,a\xd0\xe2jp=\x93O\x00\'\xb6+ sW\x80\xbb\x12\x10\xf0,Q\xcd\n\x84\xed\xa41,\x90\xa7\x9fO\x93S\xd2\xea\x19\x018\x12V\xb720>-\x81\x7f\x00h1C}\xce\x80\x0c\xbf\xa9R\x06\x00\x8e\x8b\xc2b\xc9\xa7\x12\xf8\x14\x02\xa7y\xccA\x84\'\x03\xb9\xfa\xceT\xbb\xe9T\xcfw\x80+\xc3j\x0c\x01\xf7\xa4#\xa8z\x87A\x02\xac\x1f+\xc7\x0c\x02\\\xc3\xaa;\x13\xf4@\x02\xd2\x99\xa0\x11\xbf\x17\xcc\xe5A\xe9\xe8\xaev]_\x01\xae\n\xd3\x1b\x00]\x99\xae\x80\xf4\x19C\xbd\x91\xc2p\x9c\xac\xe1,\x01\xac{\x12\xa2\xbb\xe7i\x12\x11\x96\x04ru\xb74\xd9\xec\xab\x9e\xbeD1VU\xe54\x15L}}\x11l7\xa0\x9e\xd1\xa0\x8d>p\xcb\x16\xc0\xb7\x10\xf8X\x9f\xd4I\xf8>\x98\xab[\xf8\xd0\xfb\xe8\xb20m\xaa\n\xd3\x9b\x00]\x916\xa3\x04\x06j*\x83>\xf6\xc1\x8a\xb3\x000w$\xe8\x1b|Q\xe5~\xcb#\x84\x03\xb9:/]\x9d\xa6-U$\xac\xc62\xf0\'\xaf\x82\xac\xff\x16\xe5-[\xa0\xd9\xa1\xcd\xd0$Y]*\x05\xd4S\x1aH\x17\xe3,\x00\xac/\'\xf0\x19\xce\xaa|\xe9\x9f\xbc\xf0\xc6\xab\xe94\xaf:\x02\xf8\xc3`\x88\xfby\xaf\xb7\xbfFZ\x00G\xc2j\x04\x03#\xbd\n\xf0z\x01/\xbbz\x08w\xb9s\x08\x15\x8d\x1dA\xe78\xd5W\xaf1\xe8\x8b4\x11\xce4\xc0G\x00\xfa6\x05N\xfa\x9a\x02\xb3\xe6aE\xefA\xba\xd35W\xd2\x9c\x97\x9f\xa2\xb3\xbc\xea\x8a\x19O\xe6\xe4\xa5>\xbbN\x19\xe0\xcaR5\x92\x14Fx\x15\xf8\xce\x07x\xc1\xd3/\xf2\xe9R\xef\xd0fX\xbeu\x95\x12_\xaa\xa4$\xe0\n\xc8iQ\x86\x01\xe6\xf3\x08\xfa"g5\xf6\x1e\xa8\x8bf\xcdG\xf4%\xee\xd2\t\x9f/\xf9Dy>\xebf\xc6\xc39y\xfa\xfeT\xf4\x90\x12\xc0\x912u\x0b\x13\x9e\xf3\xda`\xcf~z\xee\xfcE83\xb1\xde{\xafP\xf1%})\xb9\x7fU\x15\x10\x18\xaf\x81R\xaf-%\x94\xcf0\xc0\x91\xdb\x15pTr\xf9vnG\xa4E\'\xbd\x8b\x19\xcd\xe2%\x1a7\xc2\xd7?\xacU\xc7z\xed\x111\x86\xa4\xb2\x19\xe2\x19\xe0\xbda\x9c\xaeHM\x03{[\xf1\x1dy\xa2^\xbce\x1b\xeaL\xff\xbb\x9d\x8c\xd9\x0b\xa7\xaa\x9e\x8eV\xfc1C&\\)S\x06\x01\xe6\x93\t\xfajg\x15\x8e{\x80\xbf\x1f\xfa"7O&\xfb\xee\r\xea\xc7\x9c \x0e\xb1\xee\x17a\xbbf\xdd\xd7\xeb\xb6\xa6\'\x80\xf93\xe4D\xda\xd04\x80z[\x0b\x06\xa0\xe5\xf1z\xe1\x0f;\xe04\xc9\xa8\xdaX\xac"\x87\xb7B\xc3\xa4\x93\xad\x8d\x80zR\x03\x11/-f\xc7\x82\xf5\xaf\t\xdc\xcdY\x85\'w\xd5\x15_~\xe70\x89$l\xffn\x85\xda\xd3\xe20\xb4\xb6\xef\x19\xcf\x08\x94r_/\x07\x14\x9e\x00\x8e\x94\xabq\xcc\xb0\xdeN\xab\xa8\xc0\x0f\xed\xba\xe9\x95.\xe0F\xfb6\xfcZ\xfav\xe4c\xe40\xd0\x01\xeaM\x06-L\xd1\x8a3e\xc1\xad\x81\xc8\x1f\x15\x90\x93\x1c\x9e\xa9\x93\x18\xfd\xeev\x979\x10\xc0\xb7k\xe6\xab\xcavm`=d\xcb)T W\xdfe\xfbRX\x03\\U\x16\xb8\x06\xc4\xaf\xda2^\xb3\x1e\xabz\\\xa0w\xec\xac0;\xd0\x1d\xd5\x1c[\xd7\xaeP\x8eg4r,\xa8&\xd4/\x80\xb9\x0fA\xf7qV\xdf\xe0~\x1a\xff^d\xd6V\xc3\x86X\xbep\x9a\xa2\x13\x8f\xc7\x89\xe6\xd2\xb1\x12L\xd7\xda\x9e\'[\x01\xcc\x9b\x10\xd2\x115\x93\x19\xc7\xd9\x08Q\xfe\x1d6w\xf8\xa9\xde\xba{7\x8e\xb7)/e>\xfc+\xa1\xefU\xce\xe2\xc8\x9a\x98R\t(\xc9\x90\x05\xeb;\x158\x94\xbcw%+\x81\xf6\xbd\xc5\xab\xc0\x8e\x1a5\xc2\xaa\xd5\xf3T\xcb\xdc\xd6v.\xc2\xe24\xa0\x02\xba\x97\x8dg\x88\x15\xc0Ua\xf5w\x00\xb7\xd9\x89\x0bt\xbf@\xcf*^\x8e\xb3m\xcbK\xb9_\x9f\nL\xfc@\xdc.\x92\x13\x151\xd4\xfb)Xq\x06\x00\x96cB=\xd8Yu\xa3n\xd7\x18\xf5\xb6\x97\xde\x03\'w\xc6\xacE\xffU^t6>\x18\xd2\xb7\x9bZ1\x02\xcc\xe5\x81K"\xcc\xef\x9b\x18\xc5\x9f\xdfq?\x17\xfe=\x9f\xcf\xb5-\x9fX\xael\x9eB\xeb\x9f8\xd4\xdc\x06\xa81\x1a\xe4u\xb2\x95\x01\x80\xf5\xb5\x04\xee\xe2\xac\xbacO\xd0\xf8\xe6\x07\xef\x1a\xb8\xfd\x06*|r4Y\xeb.@t\xa9\xc9\x91\xcf\x15`f\xe4D\xca\x033\x01\t\xf02\xd3\x94\xe9(\x1ep\xad\x16\x9f\xab\xa43b\x13\x87Q\xbf$\xdc\xf7\xa4\xcb0\xfd\x16\x83\x16x\xb4b\x9f\x01\xe6#\x01}W\xcc\xb9+I\x87\xfe\xfd4c\xf0\xc3\x1ee\xdc\xcfgO\xc1\xabje\xbf>\xb6qW4/\x90\x1b\xe9\xe5\xe6\x92\xeb\n\xb0\x97\xdd\xaa\x1d;Q\xd1\xbe\xbb^\xb7}\x07\xba\x98\x80tz\xde\xa1\x05\xb0\xe2K\x97az5C\xbd\xe0Qy>\x03,\xbbV\xb2{\xe5D\x17\xf5\xd2\x98\xbe:U\r\x00\x875\xc3\xb2\xf5\x8b\xd4\xd1\xcd\x9a&_^\xd5\xe6L\xc0\xc8@H?\xe8\xf8isz\x10\r\xfc\x82Z\x04B;\x1bq/\x19\xac\x0b?\xfa\x04\xd6\xc3\x8b\x13\xcf\x82G\x08\xfd\xaesV`\xe0i\rl\xb0\x91(V\xc6o\x80\x87*\xb0C\xb4\xd4\xb29\xc0)\x97\xdbO\xae\x9cz\xf1\xf3\x9f\xa1\xf0\x83\xd7\x94\x9d.\x19\x1bvAww\x8a\xa0p\xd4deX\r%\xe01\x1bUN\xfd\x14K\xfb]\xa5O\xb2)k*3\xa0\x0b\xf0\xf6t\x17+\x9e\xcdP\x05\x1e\xac\xd8G\x80eSC67\x9c\xe8\x0f\x835\x9e\xf9\xc4\xd4C\xbb\xe7S&\xa9\xa5\x17\x9e\x07+\x9d20,\'\xa4\xc7$\xe3\x9cTZ.C\xe3*\xa8E\xb6>\xcc\xc7\x9c\xa6\x17|[\x82\xe8\x01\x82\x1f\xf4\xcdL\x856\x1d\x1c8\xed\x00\x02\x8fj{w\x1e\x1f\x01\xd67\x12\xc4\xbb2\x191\x03-~\xa2\xb1\xd3\x0f7#\x00G\xb5\xc5\x82\xb5\x0b\x95\x95N%\x16*\x08\xdd=Y\xc0[Ri#au;\x03O\xdb\x805r,\xcfzh\x1c{\x99\xde\x1b\xd9\x0e\x1f\x04\x8c|\xc6\xd9\x8a\xd5\xdb\x0c\x9aoi\xc5~\x01\x9c\x0bDdr\xe5@\xcf\x8db\xdc\xfe\xac\xa5LF\rT\x17\x18~\x17\xcd\x1ay\x0fY\xe9\x96\x80\xdf\x07BZ\x96\xb35\xc8\t\xe0E\x8c\xba\x07\x03\xb5+o\xda\x8c\xad\xed{\xe8\xed{\xf6\xe0hK\x99\xad\x8a\xb5m\n\xac_\xed2L\xaf\x03\xd4\xb3\x96\xdf:\x9f\x00\xd6\x17\x13\xb8\xb7\xf3\xf0|Z7\x8d\xc5\xe9x\x7f&\xd1L\xc3\x86X\xb7\xfe3uX\xab#\xcc\x9e\xd8\x12\xba\x1a\x08\xe9\xeeF\x80c\xc1\xd7\x056H\\\x7f\x07\xcf\x98\xf8o\xf6t\xf0`\xc3W\xca\xbc=\x8a0\xe0f\x97%\xd3\xdf5\xe8\xdb\xe4\xdcX\x0e\xe7\xda\x10\xb8-\x009\xa7jN`Y?\xc7\r\x8c\x00\x12\x7f\xe6\n\x06f\xa0z\x87\xac\x94A;\x9c\xa5\x8b\xdc\xaf\x1c=&gM\x06z\xdfb\xf9\xc2\xd9* V\xee\x97\x03i\xc6k\xcf\xda\x1d\xee\x04\x88\x06\xd4\x0eB\xaf\xa3\xc1\xaa\xb0z\t\xc0\r6r4;Z\xaf\xde\xfd#\x9c\xbe\x966,\x1c\xcb\\x<0\xa5\xd0\xc5\x8a\xe70\xd4{\tC\xe2\x11\x88~\x1f\xa3\xd1\x07\x0e\xdfI\x93@\x12-\xb1/j"!)\x83iruu?\x8d\xd7-\xf6\x9dM\xed\'{\x1e\x0c\xa2\xa4\xacX5m\xd9\x02I\x8f\x1dk\xd5\xc9\x0f\x86\xf4\x8d\x89\xffV\x03\xe0X\xf4\x9f\xc4\x0f\x18\xd3&<>\x9e\xe7\xdc\xfb\x10{vA\xf1\xd2\xc95\x1f+\xb4w\xd8\x82\xa7=\x80\xfa\x8b\x06\xf6"\xeaQ\xe1\xb66\xf5\xd2f\xbc,\xcdd\xa8O9\x1a\xef\xa4o"\xf0\xf1\xc9G\x93m\xe5@\xabn\x99\xb1\xde\xb8,7_C\x85\xcf\x8e1\xefpI:\x89\n\xd6\x9d\x12\x97L5\xa4\x8e\x05d\x8b\x05\x1b\xa9}w\xbd\xb0$\xecx\xc6k\xacoS`\xd8%\xc0\xe8\x17\\&[\xef0\xf8Lr\xdc\xf4\xb7i\xc3\xb5\xcc\xf7\x88\x82\xac\x079\x7f*\x1e\xbd\x931\xfcu\x7f\'W\xb5e:\xa4!\xbe\xde\xb2R\xb5m\xd8\xd0b\x87\x90\xe8\xc6`n$\x7f\xdf\x8b\x9a\xc8\xac2L\x056A\xd9S?Aq\xbf\xc1:\xe3i\x8c\x0e?\x04\xd8\xb8\xce\x19\xe0\xb4\x01\xf4\x81\xc1\xd1\xc7klp\xf9v\xfb\xd0D\x94\xc5\xddCh\xe6c#\xa8\x97\x89\x9fd\xff\xc9\t\xf1\x80:\x00WG\x02\xaa\xf5&\x06\xf2\xfc\xbc\x81zf\xd1|\x18\x1b\xb3\xe1e*\xf3\xfa\xfd\x84+n7\x9e\x89\x98\xd8d\xe4\xf9\x07\xf9\x8c\x81\xf7g\xd6z\xe3\x82\x9b\x1c\x14k\x18*\xeb\xf6\x8d\xf2\xf0\x8d\xfc\xdb>\xcdI\x806\x88\x8dA\xc9\x95U\xa8<\xf4\x18]^Yi\xb7\x85\x99\xaef\x7fv\x0c0mv\xfd\xb4\xe2K\xce\xd5\xf8hU\xba=\xb4\xaf?{\x8aZ{Fw\x1cc\xac\xc1tM0/\xf2\xcf\x9a\x00\x97\xab\xe7\xc1\xd1\x14F\xae\xf4\xe2D\x9e?d(K\xdc|\xd6h\xc5\x14\x85\x0euVx\x16\xcdK\x84\x7f1C\xd2\x94\x91\x04\x87\xc7\x13\x1b5F\xb5\x1fsK\x80;\x13\xac\xe6\xa7\xb5\x9a[\xbf\x148\xaeof\'W\xb5{x\xd3`\x9a\xfb\xdc\xe3T\xc3+5\xa9\x16\x08\xff\x08\xe6\xea[j\x00\x1c\t\xab/mbyO\xbfP\x17-*\xae\xf6\xf3\xcd\x16\xdd\xd5\x17\x18\xf3\x8a\xbd\x15\xd32\x06-\x89\x81k!$w \xf0\xc9p\x8dN\xa8\xcd\xe6\xde\xeb4\x1e\x9fj\xc1\xdc\xc7"G\xb6Bqi\xb12\xce}\x08X\x11\x08\xe9\xe8\xfa#:D\xef\x0e\xa3}\x0e\x94$Cp\xa5\xed?`G\xabNz\xb7\xd6^<\x01M\\\xcd\xcf_\x18B\xb8~\x84\xf9;,g\xc5J\xf6\xe0\xd6\xd6\xe2)\x07\x98\x12\xd6\x19\x0f\xed\xdc\x0e@~\xcbj\x96\xe36r\xf2\xed\x1e\x86\x12\xaf\xf1\xf2\x83\x8c\x9b\x9f\xcb\xce\xf77Q\xcaM+\xd4\x8e\x16\xcd\xf7\xfbY;i\xaf\x12\xfa\xe8F!\xac\x8fjmo8p\x9d\x02\xbflR\xf5\xe3\xcf\xf2\x9c{Gev\xed[[\x86_v\x01^s9]\x8a\x97\xa7i\x0c\xf5\xdf\x04\x85\xb7\x07\xd0Cf\x84\x80\xa3:d\xf6\xfb)\x80\xcf\x00$L/\xb9\x17A_b~\xa1\x06\xf7\xd1\xf8w\xad\x97\xc4\xa4\xc3t\x9f?\xf6\x7f4\xef\xee\xdf\x91\xd1\x01C\x83\xaeo\x10\x8aL\x88\xf6\xa2\xb2\\=I\x8c?\x9a\x1a\xef5@\x17\xcdY\x90\xbd\xe1\xb9EC\xa0h\xa2BG\xc3\x07\xa1F\x0c\x93\xf8fJ\x10\xab\xfc\x82\xa6\x1e\xc5\x9eW\x01\x98\x16\xfbIv\x1e\xd9\xd5\x0c\x01\xe2X\xe7F_\x15\x01\xe7\\\xa3\xb1m\x8fe;>\x14;\xb3\x07f\x16\xbd\xaflV0\xcf\x06C\xfa\xd6(\xc0U\xe5T\x006gs\r\x9d\xa4\xbf\xd8\xb4\x19]}\x90\xd3\x8a\xc5\xbd\x17\x03\x0f\xbd\xe4\xaed\xf5\n\x83\x96\xc7,W\xf6\x9d%\x88\xf5p+\xf6u\x0bm\x01\xf0\x16\x80\xd9\xb1G\xcd\x81\xc8}\xee\xed\x0f\xbfQ\xe3\xd1\x0fSl/\x85j-\x9a\xa3x\xd3\n\xf3w\x18\xa0\xa2`(\xd2\xab\xda\x82\xc3j)\xc1\xecj\xd3\xa0\x8d\xde\xa2u\xca\xea\xf3\xdc\x9d%o(tq\xb1^\xf5\t\x83>\x8a\x81+\x89\x0f\xfcJ~\xf0.\x00\xf9\x89%\x1b\xc2S\x96\x15\x01\xa7\xfc"{\xb3i"|_Y\xa6\x8c\xfb\xd2\x92\xd4<\x10\xd2-\xab-8\xacvBR\xdf\xbb\xd0\x9a\xb5\x08w\xec\xa9\x1d<\x81=cg\xacpUw\xe0\xd5).\x87\r\xdf\x00J\x02\xd3\x84\xc4\xcd/\xa5\xd8;\x171F\x03XY\xfd\xdc\x14\xff{m?\x8dI\x19:lH&\xe1\xda\x85*|T[\x18\xb1\xd8\x1b\xd1\xed\x88\xcb\xd1:\xc2\xca\x98,a\xd2\xdb\xbc\xe8\xda\xdb9\x95\xd5\xa8\x11\xccd\x05\xde\x7f\x98p\xd1\xf5.\xbeY\xaf0 C\xb3|s\x87\x01\xe6\xeez\x14C\x92\r\x8a\xc3\xd2V@f\xd7Z\xc2T\x1c\xe8?/3.\xbd/{3\xea\x89\xe3\xe9\xb3__F2\x85t%fu\x91\x00|F\x84\xd5<S\xe1\xdf\xde\xcd\x85\xf9\x93R\xf3w6\xf1\xae\xfd\\\xf6\xa0K\xbeR\xc8qp\xbe\x958%\x89W\x8a\xd2\xaf\x00\\\xec\xb5\x05\xcb\xf2\xf2m}\xddl\xc5\x95{\x80\xb6\x1d5\xb6\xfch\xc97\xcdb7]M\x85\xcf\x8d\xb5:]\xba\x87$aYDk\xc9\xd8\xe8J}\xae\xd4\x85\x9f\xceJ\xdfk\xd2\xd4\x8e<79\xde\x05^f@\x0e5e)\xf4\x7f\x16\xb3e\x998I\xaan\x99D\xc9\xa8.\xe9M\xc4W\xd4\x14\x17 \xb3\xebQ\xb1%T\'B\xc4eD\xb9\xbc\x8fFA\x96\x96L\xe7\x9d\x8d\xc2\xe9o\x9a\xbd.\x89\xf1(U\x95\x05.\x03\xb11\xd0\xa2ko={\xf9\xca\xa8\x7fD\xc6\xe9\xd9[\t7?\x90|x\xa6\x1f\x00\xf5P\xec\xdbk3\xb1\xfa\x0b\x00\'?\xe56\x00\x1e1t\'a\xc2\xa5\x87\xab\xea\xa4\xa5I\xe8\x85\xbf0~\xf7Lv\x86\xe9\xce\'`\xf6\x173\x9cc\xaa\xe3\xe2\x11\xe1)\x01\xd8\xea\x90\xa1]W\xfdy\xf8;s\xa4\xa0\x1f\xe8\xcf~Q\xe1\x0c\x87\xd4#4\x97\xa1\xde\x8d)R\x12H\xb8\x05^\xfeY\\q\x0c\x12\x895\xff\xcd\xa5\xcc\xd7\x00bn\xe5r.,\xe7\xcf\xc9h\xfe\x14\xa0\xe7M\xd9\x99M\x87Z\xe3\xf3\r_X\xa4\x82`\xbcD\xb1t\xfa\xc6<\x89\xcd\x8f\xd3+vV\xa4\x9fw\xd2\xe6\x05X^\xa0p\x82\x83\xc3(\xbd\xcfPE\\\xbd\x89\xb1\xefX;\t\xd7\x04\xcb3\xb6)Y3\xdc\xb6y\xe4\x08\xe6G@\x9fC\xe0K\x93\x03\xbcr\x01\xd0y@v\x00n\xda\x04+\xbe_\xa3\xcc9@\x19\xff\xa2H\xb9\xba\x83\x19O\x98\x94pH[]Z\x15\x81\x0cj\x19\xa7\x92\xd9\n\xb9\x0e\x87b\xeau\x06\xc9~\xb3\xcc\x9e\x9ft\x11E\x1cHms\xb8\x9a\x86\xea\xd80\xcf\xdd\t\xfaW\xc9\x01._\x0b\xb4\xed\x99\x1d\x80\x83\x01\x94\xfeX\xa2\xccX0\x17\x08\xc0\xf71CV}\xae\x14\x0ci9lkl*\xe7\xc7\xf3\x9dk\x14\x0eqX\x95\xab|q\x8ccD\x1du\x1d#r\x00\xdc\x11K\nn#\x90\xe4\x87v\x1b\xc3&\x00\xf8\x04pKx\xf6c\x05\xd0\xf4\xb8\xec\x00,\x07\x9fUae\xc6\x82x\xba\x17\x80\xe5D\xd5u3\xc4F\x976e*V+4l\x9a\xbcdF\x00\x16U\xb9\xe5\x0c\xb2\x00x\xcfN\xa0I\x87\xac\x01\\Q\x15Vf,\x98\xa7\xd3\xde2u\x87"\x8b!\xba\x9d.\xa9\xaa\x82x\x1ag\x9cJf)\xe4:L\x9e22D\xcb\x92\xc9m\x0c\xb3\x19\xa2\xbf\x06\xda\x9e\x9d\x1d\x80\xc5\x95\xf6\xc7\r\xca\x8c\x05\xf1{2\x8b\xbe\x19\xc4\xff0\xa1\xd6\xa2\x83\xfer\xc7N\x0fy$L\x0c]\x9e/}G\xa1\x93\x83\xdf\x82\xf5$K\x0e\x0c\x8cS\xc7\x98\x10ri\x9e[\xa6M\x8bI\xd6\x8a\xb9\xc0I\x97e\x07\xe0fM\xf1\xe5\xb6\xd5\xca\x9c\xd3\x831\x89\xaa\xca\x03W\x81\xf95\x13\x1e?\xe9\xa6\x17\x96\x96g\xd6M6.\xc3\xcc\xe7\x15\xcer\xb8\xa9\xb0\xc62I\x96AnsI\x9b\x89\x96\xb8\xed?\xe0\xd2\xfb\x15\xfb\xd7\xcan\xcb\xa49\x93\x81^\x19\x8an\xa8-]\x9b\\,\xfcf\xb12\xe7\xbe$\xbc \x16<\x10\xc4\xb1\xb3\x13\xe7\x8e\xa6\x92w\xc3\xf4\xd28=\x1fw-\xe1\x0f\x8f9\xecCW\x00\x81\x07c\x96"[\x94\xb2U\xe9F\xb2\xd3\xe5\xe4+j\x9a=\x0b_\xd9\xaa\x8c\x1d\x07FF(\xc7Y\xc8S\xc3\x18w\xbd\x9a\x9d\x8d\x0e\xdb|\x1e\x92E\x9e*7\x06\xfb\x90\xd6r\xdc\xedJ\x17_\xa5\x0b\xa7}\x9a\x9d\xad\xca\x81\x9d\x80\xb7>qqx\xff\'W;\xd3\xd9nU\x8a\xd7\x86x?\xca\xe9\x90\xbc\x1b\x92+H\xc05\x1d/&lU\x9a\x8e\r\xaf\xf8\x99\xc6{b\xedY\xa0\xbe\xe7\xa1\xf0\xc3I\xe6\xadJ\xc9qI{Kp\x8a\n(\xd9\xa9u\xa5\xa1\x0f\xf2\xccq\xcf\xb1\x8d\'\x81\x89\x95\xf1y\xf3\x06@\xc9r\x85C\x1cf\xd2\x12C\xa4^\xca\xf2a\x83K\xe2\x95\x1fw\x02m;k|\xbf\xd7\xd85_\n\xdc5\x84f\x8e\xb1p\x82\'\xe06\xe2uh\x1e9Dm3\xb5\xfc\xfeT^2\xe8:>\xc5T\xce\xaf\xe7\x93G\x13.vI\xb2\xad\xfe%7\xb1\xc46<\xe4\x1b\x9a\xaa\x17\x87\x93\xc0r0!\xb3gq\xe19\x06\x88\x0cq\x1eQ>\xccg\xf4\xcf\x92\x03\xbc\x88\xfb\xee\x04Zr\xe9\x85d\xc4\x82\xa1\xab\xb3\x89T\x95\xabm`w\xef\xe0\x8d\x9b\xb1\xa5\xcdI\xdao5:\xbe\x0fW\x9c\x04\xbc>\xcd\xe5\xc0\xff[@\xfd=\xf6-\x96#\x90\xa8\x17\xb0\x8f$3\xf0\x98\xeb\x8e\xbe\x82\xc0\xa7;\x9fM\xff\xaa\xaf\xc6[K}l\xdb\xc0\xaat\xa9\xdar\xe4\x11\xe6W:\x00\xdd:*u\xa4\\-f\x86\xf1\x8d\xc8\xb6\xcbN\xe1s\n=\xf7E\xd9\xd4\xed\xb5|\x87\xd5?3\xeb\xb2\xa3/ p_gpg\x17\x00\xe7\x0e\xc9\xce\xf2H4\xa0\x14\xb6\xec-U6\x86\xb6)\x18\x8a\x01\\UN\xef\x82i\xa0\xe9\x1d\xcc\xed\xac\x97l\xdej~\x11L|l\x9f\xdfx\x16\xf0\xfc\xdb\xeeNo5nh\x11\xd7\x1d\x89l6:\xb38H ^\x1cr\x80\x11s\xd51e\xb4\x13.\xb7\\\xae\xf1\xd2\x1c\xdb\x1e\xa5_\xee\x88\x96XR\xbe\\\x19\x8d\x11\xe0\x19\xc1P,\xa86R\xae\x9e`\x8e\xee\xde\xbaR\xaf\xfez\xe6\x9c\x85\xd9\t:\x8b\x0b\xf2\xce#\x84\xfe.i\x95\xa4\\\r\x9fh\xbf\xdcf\xe5\x1e\xa4\xdf\xb8\xfbFO\x9e\xc0\xb8\xec\xcf\xd9Y\x1a\xc5\xf5q\xd6i\x989s\xb2\x95\xdb\xec3\xc1\x90\xbe\xad\xfa\x1bl\x99I\xf6\xf9Wx\xcem\xf7f\xd7\xf1\xfd\x94\\\xe0\xb3\xc5\xe6\xb0\x95:\xb9,e\t%\xe9\xc7%\xd0\xc3\xe9\xccX\xcez\x8bc\xde\x1e\x89\x8e\xef?\'\xe8\x9f\x99\x1d\xdf{t\xd3X\xe2s^\x0e\x93\x91\x8d\x1dA\xb3\xef\x1cBf\xc7\x8bXF\xdah/x\x0b\xdaF\xf6*\xab\xf4b\xc1\x90\x16\x0fL\x87\x05\x8cI\xbc\xd4\x9e?z\r\xe1Or\x9f\x9a\x81$g\x07\xcd\x8e\xcd\xae\x13\xcb\xca\xd9\xb1xb$\x86\xaeH.IY\xe7&\x92Xmo\x02;\xe5\xcbL(\xfb\xf8P\xc6\xbd\x13\xb3k\xbd\xd2\xfc\x96Uj\xfba\xcd\xcc\xd9\xf6\x03\rt;:\x1c%\xfb\xb4V\x19V_P\xf5\xfb\xeeJ=\xfa\xea\xff.Y\x8a\x0bL\xe5\xfc|\xfe\xa7\x0b\x81G\'\x98\xad8\xdef4\xd7\xc6\xa2\xea\xbb\x0f\xad\xa8\x13Aw\x01\xf84\xf3K\x14\xe7\xf7\xe7\xeb5\xc6\x1a=\xd9\xacZ\xb7.\x94\xdb\x1a\xf3J\xbeP\xc6\xb0\x15\x06\x8asB:\x1a\xa0\xb0\x1f\xe025\x8e\xc8\x9c\xcd\xfd\xd57\xb8\xe8\x86?rV\xa3\x0bW}\xa8pL*\x97\xbd\xed\x02hi\xf5\x85\xd1I\xc3G%\x13Igr\xf4\xb3r\xd3\xfc\x81\x08\x1f\xbd\xf5\x06\x9a\xf6\xd4h\xf3\xedr\xe2\xc0\x91\x93W\x9d\x15~\x7f\x00x8p%\xc0o\xd8\xbcN\x8d\x8e\xd2\xdfTV\xc2b \xb3\xe1\xe6^\xa6\xcf\xb1\xc0\x7ff\xd9[o\xfa-\xdas\x18\xd0[cJl\xc6m_+\xf5\x92\x0b\xa7\xa9\xaf\xba\x9d\x84\x8ef\x0e\xf4\x8b`(\xf2f\r\x80\xbd|\x87\xcf\x1b\xa4\x0b\x8b\xe6eg_\xfa\xad\x07\x08\x03\xabC\xa8\xea\x1d}\xf42\xe3\x92,9\xbcK\x16\xda-\xab\x94U&\xdf\xf8\xf7\xb7\x06\xc0\xf2G}K\xc2\xd2\xba\x11P\xb6\xb6~Zo\xfcm\xebp\x82\xc6\xba\x14\x92\x7f{}[\xd3N\xc2"\r\xd6\xb74J\x0f\xf4\x07F<oH\xa3$\x91\xf9\xc7e\xc6\xc2\xe5\xfeD\x9a\xc7\xd1\xd8$\'\x1aw\x17c\xe8\xbf,\'s^Q\x8d\x95\xf7-\x8dR}K\x84\xb6\xee\x13\x85v\x0e\x07\xfa$W\xd0\x8a\x03|%\xc0r\x0b\xf7Y\x04\xb6\xcalm\xd62m@4\xb3|<\xe1iD\x0e=:&\x07y\xfbw\xc0\xe1]3\xbbU\xe9["\xb4\xa8\x15\xd7\x93T\x86\x03:\x01o\xbb\x9d\t\xcfb\xd0\xe4\x9a\x96#\tU\xb8+\xa2W\xae\xa7B\xb4D.\xc3\xc4\xfex\xe3\x18\x13\xd3\x96\xe5\xcd\x034^\xb6u\xd1\xf5(\x98\xaf\xa9\x0c\xa5\xed\xfa\x92\x8c\xf4\x83\xd1\x84\x9f\xbb\x1c\x17\x06\xfe\xe6r\xa7\xe1a\x00\xb7#\xb0\\\xb5%\x8e-n\xc9H\xe7 \x9a\xd4\x946pu\xde\x0e\x07\x8a\x0cS\x8eG\x92\x0b>\x00\xce\xba93V\xec{2\xd2\x98\x15K\xd6\n\xe3-\x99\x99J\'\xdc\xfeP`\xcdJ\x97\xa3\xc2\xc4\x03\x7f\x93E\xf8\x95N\xd8p\xaa\xd4\xf3T\x8d\xf9e&a\xbc=\xf7\x92N\x18\xc0\xe7\xc1\x90\xae\x13R\x9at,\xb3\rg\x11q3\x91\x10\xfc\x91+\t\xf7<\xe5<\xcc\xaaI\x92&\xc9rb\xe3\x13\xc0|8\xa0\xc5\x8a\x1dh\xe2\xc3\x8c\xeb\x9f\xb6\x94\xc9\x12g/\t\xc1\xc1\xb8%\x98\xa7\xebx\xc7:j\xb1*\xac\xac\xacXd\xf5;\xa5\xff\x86"\x85\x90\xc3\x1dk\xb4\xb5\xfa\xfe\xa4\xa8o\x95\r\xf9\x04\xb04\xa5\xaf"\xc7\xef;k\xa0e{\x8d\x1d\x07 \xa5\xbf\x93\xf5\x8a\xcc\xce\x00\x97\xa9\xdf\x82\xec<\x8b\xfd\xbc\x94\xe3\xd7]\x81\x89\x1f\xb9,\x8d\xa63h\xba\x07K\xf1\x11`I),\xa9\x85\x9d\xe8\xfe\xdfh<ft_\xb4y+\x01/\x97r8Y\xaf+\xc0^\xbe\xc5R\xd6\xafku\xa6\x8e%\x9c\xefr\'\xaf\x1a\xabA\x9b\xec\x94\x14-\xe5#\xc0\xc2.\xf2\x07\x05\xa7\xf8\x8e\xaf\xe6\x02]|p~\xf7t\xad\x8e\xc3\xb77\xae!\xd7\xf5\x84\x97\x8d\x8f\xdd\xbb\xb1\xeb\xa8\xeez\xcd\xb6\xef\xcd\'RN\xf0tj\t,]\xee2\xb9J\xe5\xcaw\x9f\x01\xd6g\x13\xb8\xbf\xb3\xda\x06\xf5\xd6x?\x8d\xfdiI\x93\xf4\xed"u\\\xa3F\x96\x81~\xb5\xf2C\xd7\xd6\xadq\xc1h\xbb})\x8cg\xcf\xc7\x8a\xf3\x06\xe9#5\x9b/\x91H\x06\xf2\xe3\x83\tw<\xee2\xb9\x9a\xc0\x90\xabf=\x91\xcf\x00\xf3a\x80\xbeG\x01\r\x92K1\xf9\x19\xc6e\x7f\xf1(c\x8c\x95"l\xfd\xf4]\xb5\xb1\xe7\x19vq\xd8\xb5sC\'\x93\xc8\x0cp)z\x92R\xb3l\x95:f<\xcf\xbe\xef!6{\x1c$a\x18\x9e\xa7\xd0\xca\xe9\x8c\xaa\x0c\x08\xc8M\xe0^\xc9g\x80\xa3\x93-\x97H\x7fy~BG\x8d\xaf]\xd6\xd4N]xx8\xcd\x1ez\x9b\x85\xb7F\x8c\x01k}vN\x9b}i\xdb\x92\xb25\x02\x1c\xfd\xee\x84\xd5c\x0c\x0c\xb5\xd5\xed\xa0\xeb\xf4\x8c\xf7\xa7\xc2\xd3m,\xd7\x9d\x0e\xbcX\xe02<\xc7#\xfbm\x85\x88\x97\xcb\x00\xc0|\x0cA\x0fqV\xdd\x98?0\xee\x8bg\x01\xb2\x94\xf7\xd2\x0b1\xe3\xdd\t\xcaZg\x04\x8c\t\x84\xb4$\x90r%+\x80e\x8f\xba\x11\xd4,\xdb\x9b\xd0\xa4\xc5\x8eg\xe9yk\xd6\xc1\xe8}\x10\x97\xee\xe3\'\x08\xe7:D\xcf\xcb~\xb3\x1a\xa7A\xe2\x8c\xee\x952\x00p\xd4\x8ao!\xf0\xb1\xc9\xd5\x17^\r\xb4\xebe?\xda\x1c\xd3\x1e\xf3W\xcdU\xd69\xb8\xe5\xa6\xb3\xdd\xd0g;\xddW\x98\xa8"+\x80\xa5\x82m\xb2\x96D\xe6\x1d~\xaa\x8b\xd7}c\x9et\x1d\xdd\x02\x9bV\x7f\xa9Z9a\'\x9b\xfer\xdbYJ\x94!\x80\xf9\x0cr=e\xba\xa9\xbf\xc6\x84\x85f\x89s\x8f\xc4\x8a\x92%\x16\xf96\x12Y%dt7\xb5`\r\xb00\xaa,S\xa3\x89p\x9f\x89i\xe2\xf3\xf6\xa7\xea\xafJ\xca\xdc\xbd\x10F\\G\xeb\x1fx\x84\xc4\x0f2)\xa9\x17\x19\xb4\xaa\x9e\x01\xdc\x04\xd0w8_\x96U\xf8:\xe3\xfc;\xdden\xd2\x04\xdfl_\xa3<y\xc6H@YN\x9e\xb6N\xdc\xe8\t\xe0\xa8%\x87\xe9m\x80.\xf3\x02rng\xbdz\xf3V\xc7\x0b\xb4\xaa6-UU-\x8e\xc0!Iy~\r\x04\x9e\xb7\x1f\xee\xea\xf0\xc8\x90\x05K;\xdc\x8f\xa0\xcfuVa\xf7S\xf4\xce\xe2\x8d\xc9=P\x03\n[\xf7\x94*\xf1\xe2\xf6@\xfcN0\xc4\x97{\xa8\xe0\xbc\x93\xe5\xc4Dngi@\xea?6\xe9\xff\x13y\xe4\x9e\xa8\x8b7o\xab;\\w?\x19\x85\x0b\xa6:\x87B\xd2{\x0c5\'E\xeb\x15\x012\x08\xb0\x84\xafFnu\x9e\x18\xfem\x04o\xbb\xfb\x1f,\x99\xb8\xeaPU\xd8\x9b\xa7\x8a\xa4\xe9\xdf\xcb\xfa\xa2\xf8m*\xb6 {\xb6\xe0\xe8\x9bk\x99\xfe\xb0\xb6\x10\xbd\xfa\xeb\x8f\xe7,\xc4\xf9\x89\xff>y"-\xbe\xf8\x02J\xee3\xb9\x03POiP\nK\x8e}md\x12`\x99l\xfd\x86\xaa/\xf6HB\x15\xdb\x11i\xdeIW0G\xbd\xb2\xa3\xd4\xa41\x96m\xff\xda\xce\xb7*\x91e@\xa9\x9f\xd3\x91U\x9eo\x89H\t\xe0\xe8P]\x1e\xb8\x11\xcc/\xda\xbeI\xf1r\xf7?\xcc\xd3\x1e{\x9a%\x1f\xbb\\g\xbet\xcb*\xe5x\t\xb2Jr\xa8\xef\xb5\xbd\x8cZ\xb0\xbc\xec\xa7\x12\xf4/\x9d\xd5\x98\xe8\xa0\xd8\xfd$L[0ME\xfb\xee\x85$\xce7\x10\xd2\xcfx\xa9\x13/\x9b2\xc0\xc2\xa0\xb2T\xddK\xca\x98\xed\xb1\x8e\\\x05\x1f\xf1\x82\xcb\xaf\xe7\xd3M\x81\xcc\xea9\x06\xadMcx\x96\x963l\xc1h\x04\xe8[\x15\xf8\xc8\xe4\xea\x9f5\x1f_\xf6\x1e\xa8O\xbc\xf1*\x9a\xfe\xfc_\xa9\x8fW\x90\x18\x18\x9b\x13\xd2\xd6{\x10\xb5\xf9\xa7\x05p\x0c\xe4\x91\xa4 Y#=\xd1\xb7\xa5(iq\x18\x9a7k\x9a|\x12"\xc9\xce$\'V\xda\x94i\x80\xc5\x8a\r\xb1L/O\xe2y\xd7_e\xbeH\xa3n_\xf9\xcd`\x88\x7f\x91\x8e\x0e\xd2\x068\x1d\x90\xdd\x04\xf7t\xcb\xb7\x1b\xa3,\x00,\xa7K\x91\xdf+\x97\xc3\xd7\x14 "\x9e\x16\xcc\xe5\x0bS\xa8Y\xa3\x8a/\x00\x0bG\xdb\x84j6\x02\x93\xdcT6^W\x87\x9b\xa4K\xd9\x00X&[\x83\xc5\xe1\xcf/u\xf2[\xc1\x10_\x99n\xd7\xa5\xbe_\x12Ee\xa9\xf2\x10\xfe\xe2j\xbd\x85\x0c\x9a\xe2\xc3\xf0\x9c\x8dop\xac#\xa6K\xa4m\xc1"\xe0\xf1@H\xdfc[\xdeT\xceW\x80\xfd\x02Y\xb6&\xa3~\xc9V\x01\xad\x86.f\xc1\x82\xc5_+\x1a\x99x\x1a!z\xbd|\x8a\xc4\x1a\x0f\xe6\xb4\xd1#S\xac\x9e\xb4\x9a\xef\x00\xfb\x05rtxY\xc4\xa0\x85\x00}\x9d\x865g\x10`q\xb4\xe7\x1e\xb1\x04-\x81\xf4`\xc9\x04\xb8\xbe\x0f\xd1\x89]\x94\xcd\x10\xad\xf5\x13^w\xbc\x92\xa9)z\xd9\xa4\x00-\xf74x\xa5L\x00,\xf1\xc4\xdd\xe1\xcf7\x97\xb0\x9d4\x86\x05\xf2\xb4mfMO\x1a\xc8\x88\x05\xc7%\xa8\xbet\x9a\xc6y\xdd\xbbv\xec\xc1v\x80VK\xbeh\xfb\x9bE\xfdZ\x07K\xa6;\xee\x08\xc8M\xa5\xe6\xf8z[\x0cx\x86\x06\x0fk\x10\xb2N]n\xcbx_\xb9\x8c\x02\x1co%\x95S(cO*\xab-\x9a$\xcf\xc6w\x0c\x92\\\x19\xc9f\xdd)X0K\x82\xf0\\\xf9\xc9\x99/\xc0\x9d\x08\xc81J\xe4\xa9\x00\x11\x9eP%z\x18\xf5\x90\xd3\xee\xccQV\x00\x8e~\x97\xcb\x02W3x\xb8\x17\xa7\x01\xcf\xdd\x96\x0b\xa1\xcb\xab#\xfa\xa3\x19\xea\xe4o9F\xef\xce\x80\xec\xed\xc7\x96\xaa\xe2\xc3,~\xd5\xb4\x86\xc0\x92\x86\xa1)\xaa\xa3\xfc\xe3\xa0\xc6syx\x16\xc0\\\x81\x08kX\xd3\xa8`^\xc4x\xdb\xba\x99\x9b\xb9D\xd6\x00\x16Qb\xd1\x8b\xf7xq\xff1w\xe1\xa0*1>\x10\xd4\xa3\xa9\x15$#WV(\xab\x00\xef\x1b\xb2K\xd1\x13\x8a\x86\x12\xcc7\x9efE\x0b\x19o\x84\xe6\x05\x08\xa3)7\xf2A\xc6\x9b\xaa\xd5\xc0\x01\x018.C\xcc\xef\xfaV\x9b@\xb7l+\xc6\x97\xf6\x18\x1b\x98\x91\x1f\xcc\xd3\xe2\t\x93\xd1o\xad\x93\xbc\x07\x14\xe0}@W\x87\xc9H\xe2|cD\xa3/\x8a\xcf0\x13q\x8a\x03!\x7f7\xeb|\x1b\xc7\xb8L\x8aS/\x00\xfe_\x01\x9a\xaaoH\xccW\xac\xf3)\x0fr\r\xd1\x01\xa7z\x05p\\\x1b\xb1 \xf4\x01\x04\xf4g@\xb2Y\xd5["`3\x03\x93\x03D\x05\x94\x1b\x99\\\xdf\x04\xad\x97\x00\xc7\x95$\xb3\xee\xc6*\xd0\x9fY\x0f\xa8o\x132\t\x1b!R\x05\xbbtd\xf2\x81\x1e\x86\xdd^\xaaz\rp\xa2\xe0\xd1]1\x04\xce\x81\xe2s\x88q\x8e\x1f[\xa0^\xacM\x9c\xde\x98P\x04ME\x95\x88\x14yu~\xf3\xd2\x96\x9fe\x0f\x1a\x80kwzw\x18\xed\x03\x08\xf4\x0e\x10wep{\x02\xb5\x8f^\xd3a\xc8\\o\xa1\xbc\n\x06\xd6\x11\xf1Z\x06\xadc\xa6%\x11Df4\n9\xde\xddb\xc1\xf2\xc0\x159h\x01vR\x99\xdcAQ\x99\x83\xf6\x94\x13lE\x11n\x02\x85\xc6\xd0h\xa2\xc1M\x02\xf2\xff\xd5\xb4\x8b\xb5L\x82H&B\xbb\x02\x01\xaa\x00W}\x0f\x0167\xba\x0f\xf6?C\xff\x0f{\xda7@xt\xcf\xf6\x00\x00\x00\x00IEND\xaeB`\x82')

##
# Add any hardware checks needed to test the device after initial flashing.
# This runs only once, and disables itself afterwards with the following line:
machine.nvs_setint('system', 'factory_checked', 4)

system.reboot()
