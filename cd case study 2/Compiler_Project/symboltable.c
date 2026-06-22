#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symboltable.h"

int temp_count = 1;
int label_count = 1;

char* new_temp() {
    char* temp = (char*)malloc(16);
    sprintf(temp, "t%d", temp_count++);
    return temp;
}

char* new_label() {
    char* label = (char*)malloc(16);
    sprintf(label, "L%d", label_count++);
    return label;
}
