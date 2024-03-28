
%{

#include "regexp.tab.h"
int firstline = 0;
%}


%%

[a-zEO]+	{
        if (firstline == 0 && strlen(yytext) == 1) {
            yylval.val = yytext[0]; 
            return LETTER;
            } else if (firstline == 1) {
                yylval.str = strdup(yytext);
                return MOT;
                }
            }
        
"+"	{return PLUS;}
"."	{return POINT;}
"*"	{return ETOILE;}
"("	{return PAR_O;}
")"	{return PAR_F;}

[\n]	{if (firstline == 0) {firstline = 1;};}

[ \t]	{;}
.	{return yytext[0];}

%%