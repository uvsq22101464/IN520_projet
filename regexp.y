%{
#include <stdio.h>
#include <stdlib.h>
#if YYBISON
int yylex();
int yyerror();
#endif

int cpt = 0;
FILE *file;

%}

%union {
	char* str;
	int val;
	}

%token<val> LETTER
%token<str> MOT
%left PLUS
%left POINT
%token<val> ETOILE
%token<val> PAR_O PAR_F
%type<val> expression
%type<str> expr_mot

%%


instruction:
	{
		file = fopen("main.py", "w");
		fprintf(file, "from automate import *\n\n");
		fclose(file);
	}
    expression {
	    file = fopen("main.py", "a");
	    fprintf(file, "\na_final = a%d\na_final = suppression_epsilon(a_final)\na_final = determinisation(a_final)\nprint(a_final)\n", cpt-1);
	    fclose(file);}
	    
	 expr_mot {;}
;

expression:
	    expression PLUS  expression {
	    	file = fopen("main.py", "a");
	    	fprintf(file, "a%d = union(a%d, a%d)\n", cpt, $1, $3);
	    	fclose(file);
	    	$$ = cpt;
	    	cpt++;
	    	}

	|   expression ETOILE {
		file = fopen("main.py", "a");
		fprintf(file, "a%d = etoile(a%d)\n", cpt, $1);
		fclose(file);
		$$ = cpt;
		cpt++;
		}

	|   expression POINT expression {
		file = fopen("main.py", "a");
		fprintf(file, "a%d = concatenation(a%d, a%d)\n", cpt, $1, $3);
		fclose(file);
		$$ = cpt;
		cpt++;
		}
	|   PAR_O expression PAR_F {
		$$ = $2;
		}
	
	|   LETTER {
		file = fopen("main.py", "a");
		fprintf(file, "a%d = automate(\"%c\")\n", cpt, $1);
		fclose(file);
		$$ = cpt;
		cpt++;
		}
;

expr_mot:
		
		expr_mot MOT {
		file = fopen("main.py", "a");
	    fprintf(file, "print(\"%s :\", reconnait(a_final, \"%s\"))\n", yylval.str, yylval.str);
	    fclose(file);
	    }

	    | MOT {
	    file = fopen("main.py", "a");
	    fprintf(file, "print(\"%s :\", reconnait(a_final, \"%s\"))\n", yylval.str, yylval.str);
	    fclose(file);
	    }	
;

%%