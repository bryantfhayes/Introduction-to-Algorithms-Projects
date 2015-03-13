#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <limits.h>

struct City{
    int id;
    int x;
    int y;
};

char** read_file(int* i, char *argv){
    int lines_allocated = 6000;
    int max_line_len = 512;

    /* Allocate lines of text */
    char **words = (char **)malloc(sizeof(char*)*lines_allocated);
    if (words==NULL){
        fprintf(stderr,"Out of memory (1).\n");
        exit(1);
    }

    FILE *fp = fopen(argv, "r");
    if (fp == NULL){
        fprintf(stderr,"Error opening file.\n");
    }
    for (*i=0; 1; *i = *i + 1){
        int j;

        /* Have we gone over our line allocation? */
        if (*i >= lines_allocated){
            int new_size;

            /* Double our allocation and re-allocate */
            new_size = lines_allocated*2;
            words = (char **)realloc(words,sizeof(char*)*new_size);
            if (words==NULL){
                fprintf(stderr,"Out of memory.\n");
                exit(3);
            }
            lines_allocated = new_size;
        }

        /* Allocate space for the next line */
        words[*i] = malloc(max_line_len);
        if (words[*i] == NULL){
            fprintf(stderr,"Out of memory (3).\n");
            exit(4);
        }
        if (fgets(words[*i], max_line_len - 1, fp) == NULL)
            break;

        /* Get rid of CR or LF at end of line */
        for (j = strlen(words[*i]) - 1; j >= 0 && (words[*i][j] == '\n' || words[*i][j] == '\r'); j--)
        ;
        words[*i][j+1]='\0';
    }

    /* Close file */
    fclose(fp);

    return words;

}

struct City** build_cities(char** words, int number_of_cities){
    int j;
    struct City** cities = malloc(sizeof(struct City *) * number_of_cities);
    for(j = 0; j < number_of_cities; j++){
        cities[j] = malloc(sizeof(struct City));
        sscanf(words[j], "%d %d %d", &cities[j]->id, &cities[j]->x, &cities[j]->y);
        //printf("Created City: %d, %d, %d \n", cities[j]->id, cities[j]->x, cities[j]->y);
    }
    return cities;
}

int remove_city(struct City** cities, int city_index, int cities_left){
    int i = 0;
    for ( i = city_index ; i < cities_left - 1 ; i++ )
         cities[i] = cities[i+1];
    return cities_left - 1;
}

double round(double d){
  return floor(d + 0.5);
}

int distance(struct City* a, struct City* b){
    return round(sqrt(((double)b->x - (double)a->x)*((double)b->x - (double)a->x) + ((double)b->y - (double)a->y)*((double)b->y - (double)a->y)));
}

long sum_tour_distance(struct City** tour, int number_of_cities){
    int i = 0;
    long sum = 0;
    for(i=0;i<number_of_cities;i++){
        sum += distance(tour[i], tour[i+1]);
    }
    //sum += distance(tour[i], tour[0]);

    return sum;
}

struct City** greedy_algorithm(struct City** cities, int number_of_cities){
    struct City** remaining_cities = malloc(sizeof(struct City *) * number_of_cities);
    struct City** tour = malloc(sizeof(struct City *) * (number_of_cities+1));

    int i = 0;
    int current_city_index = 0;
    int cities_left = number_of_cities;
    int tour_index = 0;
    for(i=0;i<number_of_cities;i++){
        remaining_cities[i] = malloc(sizeof(struct City));
        remaining_cities[i]=cities[i];
    }

    tour[0] = malloc(sizeof(struct City));
    tour[0] = remaining_cities[0];

    cities_left = remove_city(remaining_cities, current_city_index, cities_left);

    long m, n, min_dist, temp_dist;
    for(m=0;m<number_of_cities-1;m++){
        min_dist = 999999;
        for(n = 0; n < cities_left; n++){
            temp_dist = distance(tour[m], remaining_cities[n]);
            //printf("latest distance: %d when n=%d\n", temp_dist, n);


            if(temp_dist < min_dist){
                min_dist = temp_dist;
                current_city_index = n;
            }
        }
        tour_index++;
        tour[tour_index] = malloc(sizeof(struct City));
        tour[tour_index]= remaining_cities[current_city_index];
        cities_left = remove_city(remaining_cities, current_city_index, cities_left);
    }

    // Add the original City to the tour
    tour[tour_index+1] = malloc(sizeof(struct City));
    tour[tour_index+1] = cities[0];

    return tour;
}

struct City** opt_swap(struct City** tour, int i, int j, int number_of_cities){
    struct City** new_tour = malloc(sizeof(struct City**) * (number_of_cities+1));
    int k;
    int tour_idx = 0;
    for(k=0;k<i;k++){
        new_tour[tour_idx] = malloc(sizeof(struct City));
        new_tour[tour_idx] = tour[k];
        //printf("tour #%d: %d\n", tour_idx, new_tour[tour_idx]->id);
        tour_idx++;
    }
    for(k=j;k>=i;k--){
        new_tour[tour_idx] = malloc(sizeof(struct City));
        new_tour[tour_idx] = tour[k];
        //printf("-tour #%d: %d\n", tour_idx, new_tour[tour_idx]->id);
        tour_idx++;
    }
    for(k=j+1;k<number_of_cities+1;k++){
        new_tour[tour_idx] = malloc(sizeof(struct City));
        new_tour[tour_idx] = tour[k];
    //    printf("--tour #%d: %d\n", tour_idx, new_tour[tour_idx]->id);

        tour_idx++;
    }
    //printf("idx = %d\n", new_tour[0]->id);
    return new_tour;
}

struct City** run_2_opt(struct City** tour, long* current_distance, long* latest_distance, int number_of_cities){
    int i,j;
    long new_distance;
    struct City** new_tour = malloc(sizeof(struct City**)*(number_of_cities+1));
    struct City** temp_tour = malloc(sizeof(struct City**)*(number_of_cities+1));
    int b;
    for(b=0;b<number_of_cities+1;b++){
        temp_tour[b] = malloc(sizeof(struct City));
        temp_tour[b] = tour[b];
        printf("tour id %d = %d\n", b, tour[b]->id);
    }
    for(i=0;i<number_of_cities-1;i++){
        for(j=i+1;j<number_of_cities;j++){
            new_tour = opt_swap(temp_tour, i, j, number_of_cities);
            new_distance = sum_tour_distance(new_tour, number_of_cities);
            if(new_distance < *current_distance){
                *latest_distance = new_distance;
                return new_tour;
            }
        }
    }
    *latest_distance = *current_distance;
    return tour;
}

struct City** opt(struct City** old_tour, int number_of_cities){
    long new_distance = sum_tour_distance(old_tour, number_of_cities);
    long current_distance = LONG_MAX;
    long latest_distance = 0;
    int i;
    struct City** new_tour = malloc(sizeof(struct City*)*(number_of_cities+1));
    for(i=0;i<number_of_cities+1;i++){
        new_tour[i] = malloc(sizeof(struct City));
        new_tour[i] = old_tour[i];
        printf("new_tour id %d = %d\n", i, new_tour[i]->id);
    }
    while(new_distance < current_distance){
        current_distance = new_distance;
        new_tour = run_2_opt(new_tour, &current_distance, &latest_distance, number_of_cities);
        new_distance = latest_distance;
    }
    for(i=0;i<number_of_cities+1;i++){
        printf("-new_tour id %d = %d\n", i, new_tour[i]->id);
    }
    return new_tour;
}

int main(int argc, char **argv){
    if(argc < 2){
        printf("Please supply a filename a second command line argument\n");
        exit(2);
    }
    int number_of_cities = 0;
    char** words = read_file(&number_of_cities, argv[1]);
    struct City** cities = build_cities(words, number_of_cities);
    struct City** tour = greedy_algorithm(cities, number_of_cities);
    struct City** improved_tour = opt(tour, number_of_cities);

    int m;
    printf("%ld\n", sum_tour_distance(improved_tour, number_of_cities));
    for(m=0;m<number_of_cities;m++){
        printf("%d\n", improved_tour[m]->id);
    }
    printf("SUM: %ld\n", sum_tour_distance(improved_tour, number_of_cities));

    free(words);
    free(cities);
    return 0;
}
