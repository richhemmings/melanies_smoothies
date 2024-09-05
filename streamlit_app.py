# Import python packages
import streamlit as st
import requests
import pandas as pd
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customise Your Smoothie! :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom smoothie...  
    """
)

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
# Convert Snowpark dataframe to Pandas dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)

customer_name = st.text_input('Name on smoothie:')
st.write (customer_name)


ingredients_list = st.multiselect(
    'Chose up to five ingredients:'
    ,my_dataframe
    ,max_selections=5
) 

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutritional Information')
        #st.write(ingredients_string)
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """','"""+customer_name+"""')"""

    btn_Submit = st.button('Submit Order')

    if btn_Submit:
        #st.write(my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + customer_name + '!', icon="✅")

st.write("\nThats all folks!")
