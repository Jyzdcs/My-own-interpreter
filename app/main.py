import sys
import re

class Token:
    def __init__(self, type, lexeme, literal, line):
        
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        literal_val = "null" if self.literal == None else str(self.literal)
        return f"{self.type} {self.lexeme} {literal_val}"

class Scanner:
    def __init__(self, content):
        
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
        self.errors = []
        self.exit_code = 0
        self.source = content

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens, self.errors, self.exit_code

    def is_at_end(self):
        return self.current == len(self.source)

    def scan_token(self):
        value = self.advance()

        if value == "(":
            self.add_token("LEFT_PAREN")
        elif value == ")":
            self.add_token("RIGHT_PAREN")
        elif value == "{":
            self.add_token("LEFT_BRACE")
        elif value == "}":
            self.add_token("RIGHT_BRACE")
        elif value == "*":
            self.add_token("STAR")
        elif value == ".":
            self.add_token("DOT")
        elif value == ",":
            self.add_token("COMMA")
        elif value == "+":
            self.add_token("PLUS")
        elif value == ";":
            self.add_token("SEMICOLON")
        elif value == "/":
            self.add_token("SLASH")
        elif value == "-":
            self.add_token("MINUS")
        elif value == "\n":
            self.line += 1
        elif value == "=":
            if re.match("=", self.source[self.current:]) and self.source[self.current - 1:] != "=":
                self.add_token("EGAL_EGAL")
            else:
                self.add_token("EGAL", "=")
        else:
            self.error(value)
            
    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type, literal=None):
        lexeme = self.source[self.start : self.current]
        self.tokens.append(Token(type, lexeme, literal, self.line))

    def error(self, char):
        self.errors.append(f"[line {self.line}] Error: Unexpected character: {char}")
        self.exit_code = 65



def main():
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read() 
    
    scanner = Scanner(file_contents)
    tokens, errors, exit_code = scanner.scan_tokens()
    for error in errors:
        print(error, file=sys.stderr)
    for token in tokens:
        print(token)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
