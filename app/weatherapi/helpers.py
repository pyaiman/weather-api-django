import pycountry


def get_country_alpha_3(country_alpha_2):
    """Function to retrieve alpha code 3 of a given country"""
    country = pycountry.countries.get(alpha_2=country_alpha_2)
    return country.alpha_3