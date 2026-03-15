import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    #a function to complete child's probablity
    def chi_pro(person):
        #use p_gene's sequence to represent parents' gene
        p_gene = [0,0,0]
        p_gene[everyone_gene[people[person]['mother']]] += 1
        p_gene[everyone_gene[people[person]['father']]] += 1

        #comlete the probablity of gene
        if person in no_gene:
            situation = 0
            if p_gene[0] == 2:
                each_pro[person] = (1-PROBS["mutation"])**2
            elif p_gene[0] == 1 and p_gene[1] == 1:
                each_pro[person] = (1-PROBS["mutation"])*0.5
            elif p_gene[0] == 1 and p_gene[2] ==1:
                each_pro[person] = (1-PROBS["mutation"])*PROBS["mutation"]
            elif p_gene[1] == 2:
                each_pro[person] = PROBS["mutation"]*0.5+(1-PROBS["mutation"])*0.5
            elif p_gene[1] == 1 and p_gene[2] == 1:
                each_pro[person] = PROBS["mutation"]*0.5
            else:
                each_pro[person] = PROBS["mutation"]*PROBS["mutation"]
        elif person in one_gene:
            situation = 1
            if p_gene[0] == 2:
                each_pro[person] = (1-PROBS["mutation"])*PROBS["mutation"]*2
            elif p_gene[0] == 1 and p_gene[1] == 1:
                each_pro[person] = PROBS["mutation"]*0.5+(1-PROBS["mutation"])*0.5
            elif p_gene[0] == 1 and p_gene[2] ==1:
                each_pro[person] = PROBS["mutation"]**2+(1-PROBS["mutation"])**2
            elif p_gene[1] == 2:
                each_pro[person] = 0.5
            elif p_gene[1] == 1 and p_gene[2] == 1:
                each_pro[person] = 0.5
            else:
                each_pro[person] = PROBS["mutation"]*(1-PROBS["mutation"])*2
        else:
            situation = 2
            if p_gene[0] == 2:
                each_pro[person] = PROBS["mutation"]*PROBS["mutation"]
            elif p_gene[0] == 1 and p_gene[1] == 1:
                each_pro[person] = PROBS["mutation"]*0.5
            elif p_gene[0] == 1 and p_gene[2] ==1:
                each_pro[person] = PROBS["mutation"]*(1-PROBS["mutation"])
            elif p_gene[1] == 2:
                each_pro[person] = 0.25
            elif p_gene[1] == 1 and p_gene[2] == 1:
                each_pro[person] = 1-PROBS["mutation"]
            else:
                each_pro[person] = (1-PROBS["mutation"])**2

        #find the probablity of strait
        if person in no_trait:
            each_pro[person] *= PROBS["trait"][situation][False]
        else:
            each_pro[person] *= PROBS["trait"][situation][True]



    #find the no_gene and no_trait people,and find the parens and children
    no_gene = set()
    no_trait = set()
    parent = set()
    child = set()
    each_pro = {}   #save everyone's probablity
    everyone_gene = {}

    for person in people.keys():
        if person not in one_gene | two_genes:
            no_gene.add(person)
        if person not in have_trait:
            no_trait.add(person)
        if people[person]['mother']==None:
            parent.add(person)
        else:
            child.add(person)
        if person in no_gene:
            everyone_gene[person] = 0
        elif person in one_gene:
            everyone_gene[person] = 1
            each_pro[person] = PROBS["gene"][1]
        else:
            everyone_gene[person] = 2
            each_pro[person] = PROBS["gene"][2]

    #complete parent's probablity
    for person in parent:
        #first find the probablity of gene and save the situation
        if person in no_gene:
            situation = 0
            each_pro[person] = PROBS["gene"][0]
        elif person in one_gene:
            situation = 1
            each_pro[person] = PROBS["gene"][1]
        else:
            situation = 2
            each_pro[person] = PROBS["gene"][2]

        #then find the probablity of trait
        if person in no_trait:
            each_pro[person] *= PROBS["trait"][situation][False]
        else:
            each_pro[person] *= PROBS["trait"][situation][True]

    #complete the probablity of child
    for person in child:
        chi_pro(person)

    #complete total
    return_value = 1
    for value in each_pro.values():
        return_value *= value
    return return_value




def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for people in probabilities.keys():
        if people in one_gene:
            probabilities[people]['gene'][1] += p
        elif people in two_genes:
            probabilities[people]['gene'][2] += p
        else:
            probabilities[people]['gene'][0] += p
        if people in have_trait:
            probabilities[people]['trait'][True] += p
        else:
            probabilities[people]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for people in probabilities.keys():
        trait = 1/(probabilities[people]['trait'][True]+probabilities[people]['trait'][False])
        probabilities[people]['trait'][True] *= trait
        probabilities[people]['trait'][False] *= trait
        gene = 1/(probabilities[people]['gene'][0]+probabilities[people]['gene'][1]+probabilities[people]['gene'][2])
        probabilities[people]['gene'][0] *= gene
        probabilities[people]['gene'][1] *= gene
        probabilities[people]['gene'][2] *= gene


if __name__ == "__main__":
    main()
