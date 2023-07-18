# bCarbonZero

http://bcarbonzero.pythonanywhere.com/

*The website is designed to provide the best user experience on desktop devices. While it is accessible on other devices, such as tablets or smartphones, it is optimized for desktop usage and may offer a more comfortable and immersive experience on larger screens.*

bCarbonZero is a website that aims to incentivize and encourage volunteerism. Our platform serves as a bridge between non-profit organizations, volunteers, and vendors. Here's how it works:

Non-profit organizations can post volunteer opportunities on our website, detailing the tasks, dates, and locations where they require assistance. These opportunities may range from helping at shelters, soup kitchens, or participating in environmental initiatives such as tree planting.

Volunteers can browse through the listed opportunities and choose the ones that align with their interests and availability. By participating in these volunteer activities, volunteers earn tokens as a form of recognition for their service.

These tokens hold value within our platform as they can be redeemed for various rewards. Vendors collaborate with us by posting discounts and coupon codes for their products. Volunteers can exchange their tokens for these rewards, allowing them to enjoy exclusive discounts and benefits from partnering vendors. In addition, vendors are incentivized to advertise on our website, reaching a wider audience for free.

By creating this system of incentives, bCarbonZero motivates individuals to contribute their time and skills to non-profit organizations while also providing them with tangible rewards. This approach not only benefits volunteers by offering discounts and incentives but also supports non-profit organizations by attracting a larger pool of dedicated volunteers. Together, we foster community, social responsibility, and positive impact.

# Limited Functionality Notice: Database Unavailable

Please note that the functionality of this website is limited and primarily intended for DEMONSTRATION PURPOSES. As a student developer, I am unable to allocate funds for a live database, which means that most features requiring data interaction, such as account creation, post interaction, and content editing, are unavailable. The signup process only provides examples of pre-existing accounts for illustration purposes. While you can explore the website's layout and design, please be aware that the interactive elements are not functional. For the complete functionality of bCarbonZero, I recommend hosting the website locally by following the instructions provided in the next section. Thank you for your understanding.

# Running The Code Locally

To utilize the full functionality of the website on your own computer, please ensure that you have Python 3 installed.

Set up the environment: Open a command prompt or terminal and navigate to the directory where you downloaded the source code. Create a virtual environment (optional but recommended) and activate it. Then, install the required dependencies by running the following command:
pip install -r requirements.txt

Database setup: I utilized XAMPP to host the database. Make sure you have XAMPP installed and running on your machine. Import the provided MySQL file into your local MySQL database. This file contains the necessary database schema and data.

Update the configuration: At the top of app.py file, update the database connection settings to match your local MySQL database configuration.

Run the application: In the command prompt or terminal, navigate to the directory containing the source code and run the following command to start the bCarbonZero website:
python3 app.py

This command will start the local server and allow you to access the website through your web browser at the designated address (typically http://127.0.0.1:5000/). By running the website locally, you will be able to enjoy all the functionalities provided by bCarbonZero.
