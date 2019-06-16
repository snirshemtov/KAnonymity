import math
import numpy
from Cluster import Cluster
from Clusters import *

def algorithm2(D, k, l):
    # input: Table D||D′ = {R1||S1, . . . , Rn||Sn}, an integer k, a real parameter ℓ ≥ 0.
    # output: A clustering of D||D′ into clusters of size at least k that respect ℓ-diversity
    print("started...")

    if (diversityInputIsLegal(D, l)):
        return

    n = len(D)  # number of rows in the db
    t = n / k  # number of clusters
    Clusters = algorithm3(D, t)  # C= [C0,C1...Ct-1] while each group size is k or k+1

    minDiversity = Clusters.getMinDiversity()

    # in case each cluster is diverse enough, return the trivial clustering
    if (l > minDiversity):
        print("It's impossible to create " + str(math.ceil(t)) + " clusters with " + str(l) +"-diversity.")
        print("try with bigger k parameter or smaller l parameter")
        return Clusters

    clusterHadSplitted = True

    counter = 0
    # while clusterHadSplitted or counter < 5:
    while clusterHadSplitted:

        clusterHadSplitted = False

        for Person in D:
            PersonCluster = Person['clusterPointer']

            if not (PersonCluster.divWithoutPersonIsLegal(Person,l)):
                continue

            B = Clusters.clustersSuitableForPerson(Person, l)
            if len(B) == 0:
                continue

            # move person from his cluster to the cluster which is the best for him
            PersonCluster.removePerson(Person)
            BestCluster = Clusters.clusterWithMinInformationLoss(Person, l)
            BestCluster.addPerson(Person)
            Clusters.removePersonClusterIfItEmpty(PersonCluster)
        # end for

        print(counter)
        counter = counter + 1

        clusterHadSplitted = Clusters.spliteBigClusters(k, l)
    #end while

    Clusters.unifyClustersSmallerThanK(k)
    Clusters.printClustersToFile(k, l, n)

def algorithm3(D, t):
    t = int(t)

    # counting all the countries appearances
    countriesAppearancesHT = getCountriesAppearancesHT(D)

    # in the article this parameter called 'm' (numOfCountries)
    numOfCountries = countriesAppearancesHT.keys().__len__()

    countriesAppearancesLST = []
    for countryName, countryAppearances in countriesAppearancesHT.items():
        countriesAppearancesLST.append([countryName, countryAppearances])


    # represent Eqs.24 in the article, while Yij = Y[i,j]

    Y = numpy.zeros((t, numOfCountries))
    for i in range(t): # clusters
        for j in range(numOfCountries):    # countries
            modulo = countriesAppearancesLST[j][1] % t      # Country[j] % t
            if (i < modulo):
                Y[i, j] = math.ceil(countriesAppearancesLST[j][1] / t)
            else:
                Y[i, j] = math.trunc(countriesAppearancesLST[j][1] / t)

    permutations = numpy.zeros((numOfCountries, t))

    for j in range(numOfCountries):
        permutations[j] = numpy.random.permutation(t)

    X = numpy.zeros((t, numOfCountries))
    for i in range(t):
        for j in range(numOfCountries):
            X[i][j] = Y[int(permutations[j][i])][j]

    countriesArray = []
    for j in range(numOfCountries):
        peopleFromThisCountry = []
        for Person in D:
            if (Person.get('nativeCountry') == countriesAppearancesLST[j][0]):
                peopleFromThisCountry.append(Person)

        countriesArray.append(peopleFromThisCountry)

    clusters = Clusters()
    for i in range(t):
        cluster = Cluster(i)
        for j in range(numOfCountries):
            for k in range(int(X[i][j])):
                peopleToAdd = countriesArray[j].pop()
                cluster.addPerson(peopleToAdd)
                peopleToAdd['clusterPointer'] = cluster

        clusters.addCluster(cluster)

    return clusters




#### old code ####

def div(C):
    numOfUniqueValues = 0

    uniqueValuesHT = {}
    for person in C:
        country = person['nativeCountry']
        if (country not in uniqueValuesHT):
            uniqueValuesHT.update({country: 1})

    return uniqueValuesHT.__len__()

    # in the article this parameter called 'm' (numOfCountries)
    numOfCountries = uniqueValuesHT.__len__()


# check if the parameter l is bigger than the diversity in the DB

def diversityInputIsLegal(D, l):
    if (div(D) < l):
        print('Input diversity parameter is illegal')
        return  # f
    else:
        return  # t

def getCountriesAppearancesHT(D):
    # counting all the countries appearances and and return it
    # as hashTable from type: '<countryName, country appearence>'
    countriesAppearancesHT = {}
    for person in D:
        country = person['nativeCountry']
        if country not in countriesAppearancesHT:
            countriesAppearancesHT.update({country: 1})
        else:
            newValue = countriesAppearancesHT[country] + 1
            countriesAppearancesHT.update({country: newValue})

    return countriesAppearancesHT
