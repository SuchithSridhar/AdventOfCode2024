/**
 * I did this in C because I saw that this problem could be done
 * blazingly fast using bitwise operations and C was the perfect
 * place to do it.
 *
 * The algorithm runs in O(n) time and the constant c * n is a small
 * constant since it uses bitwise operations &, |, << in the entire
 * program.
 */
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_VALUE 100
#define MAX_UPDATE_ELEMS 100

typedef struct {
    FILE *file;
    char *line;
    size_t len;
    ssize_t read;
} LineReader;

typedef struct {
    int64_t a;
    int64_t b;
} Rule;

void init_line_reader(LineReader *reader, FILE *file) {
    reader->file = file;
    reader->line = NULL;
    reader->len = 0;
    reader->read = 0;
}

int get_next_line(LineReader *reader) {
    reader->read = getline(&reader->line, &reader->len, reader->file);
    return (reader->read != -1);
}

void free_line_reader(LineReader *reader) { free(reader->line); }

void init_rules_map(Rule rules_map[MAX_VALUE]) {
    for (int i = 0; i < MAX_VALUE; i++) {
        rules_map[i].a = 0;
        rules_map[i].b = 0;
    }
}

int parse_update(char *line, int update_array[MAX_UPDATE_ELEMS]) {
    char *token = strtok(line, ",");
    int count = 0;

    while (token && count < MAX_UPDATE_ELEMS) {
        update_array[count++] = atoi(token);
        token = strtok(NULL, ",");
    }
    return count;
}

void print_rule(const Rule *rule) {
    printf("\n  ");
    for (int i = 63; i >= 0; i--) {
        printf("%c", (rule->a & ((int64_t)1 << i)) ? '1' : '0');
    }
    printf(" ");
    for (int i = 63; i >= 0; i--) {
        printf("%c", (rule->b & ((int64_t)1 << i)) ? '1' : '0');
    }
}

void set_rule_bit(Rule *rule, int value) {
    if (value < 64) {
        rule->a |= (int64_t)1 << value;
    } else {
        rule->b |= (int64_t)1 << (value - 64);
    }
}

void add_rule(Rule rules_map[MAX_VALUE], int lhs, int rhs) {
    // lhs must be printed before rhs
    // i.e. when lhs is printed, no rhs should have been printed
    set_rule_bit(&rules_map[lhs], rhs);
}

int check_update(Rule rules_map[MAX_VALUE], int update_array[MAX_UPDATE_ELEMS],
                 int update_count) {
    Rule x;
    x.a = 0;
    x.b = 0;

    for (int i = 0; i < update_count; i++) {
        int elem = update_array[i];
        Rule rule = rules_map[elem];
        if ((rule.a & x.a) > 0 || (rule.b & x.b) > 0) {
            return 0;
        }

        set_rule_bit(&x, elem);
    }

    return update_array[update_count / 2];
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file) {
        perror("Error opening file");
        return 1;
    }

    LineReader reader;
    init_line_reader(&reader, file);
    int in_updates = 0;

    Rule rules_map[MAX_VALUE];
    int update_array[MAX_UPDATE_ELEMS] = {0};
    int update_count = 0;
    init_rules_map(rules_map);
    int lhs, rhs;
    int sum = 0;

    while (get_next_line(&reader)) {
        if (!isdigit(*reader.line)) {
            in_updates = 1;
            continue;
        }

        if (!in_updates) {
            sscanf(reader.line, "%d|%d", &lhs, &rhs);
            add_rule(rules_map, lhs, rhs);
        } else {
            update_count = parse_update(reader.line, update_array);
            sum += check_update(rules_map, update_array, update_count);
        }
    }

    printf("%d\n", sum);

    free_line_reader(&reader);
    fclose(file);
    return 0;
}
