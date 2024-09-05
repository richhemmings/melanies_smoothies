# Import python packages
import streamlit as st
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

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

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
    
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
        #st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """','"""+customer_name+"""')"""

    btn_Submit = st.button('Submit Order')

    if btn_Submit:
        #st.write(my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + customer_name + '!', icon="✅")

# New section to display fruityvice nutrition info
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

st.write("\nThats all folks!")
