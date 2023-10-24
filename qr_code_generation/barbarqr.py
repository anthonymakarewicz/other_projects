
# load the packages 
import qrcode
import argparse
# from the PIL package only import the Image function (not the whole package)
from PIL import Image
import io
from urllib.request import Request, urlopen
import re
from pyzbar.pyzbar import decode
import time
# create an alias for easier manipulation
from bs4 import BeautifulSoup as BS


###################
# Extracting images
###################

# as the html file does not provide images to extract
# by the soup.findAll("img") method, we have to create a cumbersome do-while loop
# that extract all images from 1 to N assuming that N is unknown

  
# define the get png images function that accept one positional argument, namely url_    
def get_png_images(url_):
    
    """ Extract all png images from the last directory before the png images
    
    This function assumes there is no directories below the one to extract images from
    
    Parameters:
        url_(str): The url to extract images from
        
    Returns:
        list: The list of all images from 1 to N 
        
    """    
    
    
    # declare and initialize an empty list to store the images
    images = []
    # declare and initialize the counter of the do-while loop
    i = 0  
    # set a timer to record the time it takes to execute the loop
    start_loop = time.time()
    # do-while loop 
    while True:
        # increment the counter after each iteration in the loop
        # (when an image is extracted)
        i += 1
        # try this block of codes
        try:
            # extract the url from images 1 to 9
            if i < 10:
                # specify the appropriate url 
                url = "".join([url_, "00000" , str(i), ".png"])
                
            # extract the url from images 10 to 99      
            elif(i >= 10 and i < 100):
                # faster to use .join rather than + for concatenating strings
                url = "".join([url_, "0000", str(i), ".png"])
                
            # extract the url from images 100 to 999        
            elif(i >= 100 and i < 1000):
           
                url = "".join([url_, "000", str(i),".png"])
                
            # extract the url from images 1000 to 9999
            elif(i >= 1000 and i < 10000):
                
                url = "".join([url_, "00", str(i), ".png"])
                
            # extract the url from images 10000 to 99999   
            elif(i >= 10000 and i < 100000):
                
                url ="".join([url_, "0", str(i), ".png"])
                    
            # extract the url from images 100000 to 999999    
            else:
                
                url = "".join([url_, str(i), ".png" ])
            
            # download and print the runtime to extract the first image
            if i == 1:
                start_first_im = time.time()
                req = Request(url = url, headers = {'User-Agent': 'Mozilla/5.0'})
                html = urlopen(req).read()
                end_first_im = time.time()
                print("It took {:.2f} seconds to dowload the first image".format(end_first_im - start_first_im))
                print("So we must wait ...")
                image = Image.open(io.BytesIO(html))
                images.append(image)
                # go to the next iteration
                continue
                
            # specify the request to send to the servor using user-agent to prevent from HTTP Error 403
            req = Request(url = url, headers = {'User-Agent': 'Mozilla/5.0'})
            # read the html page from the request
            html = urlopen(req).read()
            # convert the binary file to an image
            image = Image.open(io.BytesIO(html))
            # append the image at the end the of list of images
            images.append(image)    
      
        # if an UnidentifiedImageError message occurs from Image.open (all images extracted), stop the loop   
        except:
            # take the time it has passes from the timer
            end_loop = time.time()
            print("It took {:.2f} seconds to dowload all images".format(end_loop - start_loop))
            return images
            
 
            



#########################
# Analysis of the results    
#########################        

## print the docstring
#print(get_png_images.__doc__)

## assign the result of the function call to the images variable
#images = get_png_images('https://chifu.eu/teachings/mfr/rabrab/')
        
        
#print("We have succesfuly extracted", len(images), "images")

## plot the first image 
#images[0].show()  #index 0 for the first element
## plot the 18th image
#images[17].show()  #index 17 for the 18th element
## plot the last image
#images[-1].show()  #index -1 for the last one




#####################
# Analysis of runtime
#####################

## see why it takes too much time to run using line profiler
#%load_ext line_profiler
## comes from the urlopen (99.9% of the function execution time)
#%lprun -f get_png_images get_png_images()




#####################
# Decoding the images
#####################

def get_decoded_images(images):
    
    """ Decode images from binary files and return them as a string
    composed of digits and letters
    
    Parameters:
        images (list): A list of images extracted form the get_png_images function
    Returns:
        list: A list of strings of decoded images 
    """
    
    
    decoded_images = []
    for image in images:
        decoded_image = decode(image)
        for i in decoded_image:
            decoded_images.append(i.data.decode("utf-8"))
    
    return decoded_images   
   

#decoded_images = get_decoded_images(images)





#####################################
# Generating the key and paragraph id
#####################################


# intermediate function
def generate_prime_numbers(lower = 1, upper = 100):
    
    """ A prime number is a whole number greater than 1 
        whose only factors are 1 and itself.
        However, 1 is neither a prime number nor a composit number
        
        Parameters:
            lower (int): The lower value to generate prime numbers from (defaults: 1)
            upper (int): The upper value to generate prime numbers from (defaults: 100)
        
        Returns:
            list: A list of prime numbers
    """
    
    
    prime_numbers = []
    # add + 1 in the 2nd argument because range(1,N) generates from numbers form 1 to N-1
    for number in range(lower, upper + 1):
        # prime numbers are natural numbers (positive) and larger than one
        if number > 1:
            # we take each number from 2 until the number before, as a number is divisble by itself
            for i in range(2, number):
                # if a number is divisible by another number than 1 or itself, it is a composit number
                if (number % i) == 0:
                    # so exit the loop as it is not a prime number and go back to the first loop
                    break
            else:
                # else it is a prime number
                prime_numbers.append(number)
                    
    # return the list of prime numbers
    return prime_numbers


        
        
    
# function that check the validity of an image  
def is_not_prime_number(decoded_image, lower = 1, upper = 100):
    
    """ Function that check weither the sum of digits in a decoded string image 
    is a prime number
    
        
        Parameters:
            string_image (str): An image represented as a string
            lower (int): The lower to generate prime numbers from (defaults: 1)
            upper (int): The upper to generate prime numbers from (defaults: 100)
        
        Returns:
            bool: True if not a prime number, else False
    """
    
    
    # declare and initialize an integer to store results (always initializing a variable)
    sum_numbers = 0
    # take a list of prime numbers from lower to upper
    prime_numbers = generate_prime_numbers(lower, upper)
    
    for char in decoded_image:
        # check if each character is numeric
        if char.isnumeric():
            # if yes convert it to an integer and add it to the sum
            sum_numbers += int(char)   # shortcut for sum_numbers = sum_numbers + int(char)
            
    # stop the function call as soon as one return command is executed        
    if sum_numbers not in prime_numbers:
        return True
    else:
        return False
    
           
    
    
def get_valid_images(decoded_images, lower = 1, upper = 100, list_compr = True):
    
    """ Obtain all valid images, namely the ones where the sum of its digits
    is not a prime number
    
        
        Parameters:
            decoded_images (list): The decoded images composed of digits and letters
            lower (int): The lower value to generate prime numbers from (defaults: 1)
            upper (int): The upper value to generate prime numbers from (defaults: 100)
            list_compr (bool): Specify whether using a list comprehension (defaults: True)
        
        Returns:
            list: The list of all valid images
    """
    
    
    # much faster  
    if list_compr == True:
        valid_images = [dec_im for dec_im in decoded_images if is_not_prime_number(dec_im,
                                                                                   lower, upper)]
        return valid_images
        
    else:
        valid_images = []
        for decoded_image in decoded_images:
            # if the sum of its digits is not a prime number append the result to the list
            if is_not_prime_number(decoded_image, lower, upper):
                valid_images.append(decoded_image)     
                
        return valid_images  
    
     
       
#valid_images = get_valid_images(decoded_images)   
    

    
    
def build_paragraph_id(valid_images):
    # declare and initialize an empty string to store the results
    paragraph_id = ""
    # take the first valid image
    first_valid_image = valid_images[0]
    # regular expression to find all lower and upper case characters
    string = re.findall("[a-zA-Z]+", first_valid_image)
    # iterate over the string 
    for letter in string:
        # concatenate each letter
        paragraph_id += "".join(letter)
    # finally return the paragraph id
    return paragraph_id    
 

 
               
    


    
    
def build_secret_key(valid_images):
    # declare and initialize an empty string to store the results
    secret_key = ""
    # iterate over all valid images
    for valid_image in valid_images:
        # extract only digits using regex
        digits = re.findall('[0-9]+', valid_image)
        for digit in digits:
            # concatenate each digit from all valid images
            secret_key += "".join(digit)
           
    # finally return the secret key            
    return secret_key
    
    

#secret_key = build_secret_key(valid_images)    
#paragraph_id = build_paragraph_id(valid_images) 
#print(secret_key)
#print(paragraph_id)





def build_hidden_link(url, secret_key):
    # build the link from the url and the secret key
    hidden_link = "".join([url, secret_key, ".html"])
    return hidden_link

#hidden_link = build_hidden_link("https://chifu.eu/teachings/mfr/rabrab/", secret_key)



def extract_text_paragraph(hidden_link, paragraph_id):
    # specify the request to be sent using the hidden link
    req = Request(
        url = hidden_link, 
        headers = {'User-Agent': 'Mozilla/5.0'})
    # read the html file
    html = urlopen(req).read()
    # transform into structered data to extract html elements
    soup = BS(html, "html.parser")
    # find the paragaph where the id matches the paragraph id
    paragraph = soup.find("p", {"id": paragraph_id})
    # extract the text paragraph
    text = paragraph.text
    # return it
    return text


#text = extract_text_paragraph(hidden_link,paragraph_id)




def create_QR_code(text):
    # create an instance of QRCode class
    qr = qrcode.QRCode(version = 1,
                       box_size = 10,
                       border = 5)
     
    # add data to the instance qr
    qr.add_data(text)
     
    qr.make(fit = True)
    qr_code = qr.make_image()
    
    return qr_code






###########################
# Command line interraction
###########################

# set a timer to record the running time of the all code
start_glob = time.time()


# define the argument parser
parser = argparse.ArgumentParser(
    description="Create a QR code from website images",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
# define the url parameter with its short and long format
parser.add_argument("-u", "--url", help = "Url to retrive images from")
# define the output parameter with its short and long format
parser.add_argument( "-o", "--output", help = "Filename for the QR code", action = "store")

# extract all arguments
args = parser.parse_args()

# access the url argument entered by the user
url = args.url

# access the output argument entered by the user
file_name = args.output



# exception handling for the url positional parameter
if not url:
    parser.error('Please specify a url with the -u or --url option')
   
 
# exception handling for the output optional parameter
if file_name is not None:
    # verify its validity (it must have the .png extension)
    if file_name[-4:] != ".png":
        # it is not valid stop the code to avoid downloading images for nothing
        parser.error('Please specify a valid .png extension')
    
 

# define the main function with the url positional parameter
def main(url):
    images = get_png_images(url)
    decoded_images = get_decoded_images(images)
    valid_images = get_valid_images(decoded_images)
    secret_key = build_secret_key(valid_images)
    paragraph_id = build_paragraph_id(valid_images)
    hidden_link = build_hidden_link(url, secret_key)
    text = extract_text_paragraph(hidden_link, paragraph_id)
    qr_code = create_QR_code(text)
    return qr_code


# return the output of the main
qr_code = main(url)


# if an argument for the output parameter is entered and valid
if file_name is not None:
    # save the QR code from the file name
    qr_code.save(file_name)
else:
    # if a filename is not entered, save it as QRGret.png
    qr_code.save("QRGreat.png")


# in any case, plot the QR code
qr_code.show()

end_glob = time.time()
print("The code took {:.2f} seconds to run".format(end_glob - start_glob))



