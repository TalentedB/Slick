import argparse
from Evaluator import Evaluator
from Environment import Environment
import rich
from lark import Lark

VERSION = "1.0.0"
LANGUAGE_NAME = "Studium"
LANGUAGE_EXTENSION = "stud"

def main():
    banner = (r"""
                   ,----,                                                                
                 ,/   .`|                                                         ____   
  .--.--.      ,`   .'  :                ,---,       ,---,                      ,'  , `. 
 /  /    '.  ;    ;     /       ,--,   .'  .' `\  ,`--.' |         ,--,      ,-+-,.' _ | 
|  :  /`. /.'___,/    ,'      ,'_ /| ,---.'     \ |   :  :       ,'_ /|   ,-+-. ;   , || 
;  |  |--` |    :     |  .--. |  | : |   |  .`\  |:   |  '  .--. |  | :  ,--.'|'   |  ;| 
|  :  ;_   ;    |.';  ;,'_ /| :  . | :   : |  '  ||   :  |,'_ /| :  . | |   |  ,', |  ': 
 \  \    `.`----'  |  ||  ' | |  . . |   ' '  ;  :'   '  ;|  ' | |  . . |   | /  | |  || 
  `----.   \   '   :  ;|  | ' |  | | '   | ;  .  ||   |  ||  | ' |  | | '   | :  | :  |, 
  __ \  \  |   |   |  ':  | | :  ' ; |   | :  |  ''   :  ;:  | | :  ' ; ;   . |  ; |--'  
 /  /`--'  /   '   :  ||  ; ' |  | ' '   : | /  ; |   |  '|  ; ' |  | ' |   : |  | ,     
'--'.     /    ;   |.' :  | : ;  ; | |   | '` ,/  '   :  |:  | : ;  ; | |   : '  |/      
  `--'---'     '---'   '  :  `--'   \;   :  .'    ;   |.' '  :  `--'   \;   | |`-'       
                       :  ,      .-./|   ,.'      '---'   :  ,      .-./|   ;/           
                        `--`----'    '---'                 `--`----'    '---'  
        """)

    parser = argparse.ArgumentParser(
        prog="studium", 
        description=f"{banner}\n a tiny teaching language made by students, for students."
        )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Narrate decisions while running (learn mode)"
    )

    parser.add_argument(
        "--debug",
        type=bool,
        help="TEMPORARY BE DOING DEBUG STUFF - REMOVE!"
    )

    parser.add_argument(
        "filename", 
        type=str, 
        help="File to process"
        )

    args = parser.parse_args()

    if not args.filename.endswith(f".{LANGUAGE_EXTENSION}"):
        raise Exception(f"Invalid file extension type, please only use .{LANGUAGE_EXTENSION}.")
    
    with open("EBNF.lark") as f:
        grammar = f.read()
        parser = Lark(grammar, parser="lalr", start="start")

    
    with open(args.filename) as f:
        text = f.read()
        tree = parser.parse(text)

    if args.debug:
        try:
            import rich
            rich.print(tree)
        except Exception:
            print(tree.pretty())

    env = Environment()

    Evaluator(env).transform(tree)






if __name__ == "__main__":
    main()



