patent-corpus2question
===============

This repository presents `patent-corpus2question`, an application of the original study of [corpus2question](https://github.com/unicamp-dl/corpus2question)


## The method

Explained in the original repository project of the [corpus2question](https://github.com/unicamp-dl/corpus2question)

## The dataset

### Prepare USPTO dataset:  
Download Dataset from USPTO website: [USPTO Artificial Intelligence Patent Dataset](https://www.uspto.gov/ip-policy/economic-research/research-datasets/artificial-intelligence-patent-dataset)

However, as the [USPTO documentation](https://poseidon01.ssrn.com/delivery.php?ID=934115017026001122110093103076101087004000029032026050076123027006092103102107122100121056010047106017007064031070072072028068061005033048047068005072112114110123072086015001005098119083027021003001094008072110029104095108082019126016091114078023125008&EXT=pdf&INDEX=TRUE) shows, the dataset has a lot of patent types.
Then, it was made some filters in order to extract the patents most related to the 8 ai topics above:
1. Knowledge processing
2. Speech
3. AI hardware
4. Evolutionary computation
5. Natural language processing 
6. Machine learning
7. Computer vision
8. Planning/control

Moreover, it was extract only patents (and not pre-grant patents (PGPubs)) issued from 2010 to 2020

Finally, the document_id as it was set in the original dataset is not complete to make the request on the google patents API, since it does not start with the "US" initials.

## The abstract

Unfortunately, the original dataset does not have the abstract, an this information is important to the work, so, it was used a Python Library in order to make request to the Google Patent Engine and recover the patents abstract.

## Results over the uspto patent dataset

In progress
