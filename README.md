# ECOMMERCE API
> | Contents | |
> |-----|-----|
> | [About](https://github.com/EricHoward27/ecommerce-api#about-surveyus) | [Technologies Used](https://github.com/EricHoward27/ecommerce-api#technologies-employed) |
> | [Routes](https://github.com/EricHoward27/ecommerce-api#catalogue-of-routes) | [Future Iterations](https://github.com/EricHoward27/ecommerce-api#future-iterations)|
> | [ERD](https://github.com/EricHoward27/ecommerce-api#entity-relationship-diagram) | [Links](https://github.com/EricHoward27/ecommerce-api#links) |
> | [Planning](https://github.com/EricHoward27/ecommerce-api#planning)| |
>
> ## About ECOMMERCE
> The _Ecommerce_ API is the backend connection between the [_Ecommerce_](https://github.com/EricHoward27/ecommerce-client) client side and the [PostgreSQL](https://www.postgresql.org/) database. This API utilizes multiple models: a User model, a Order Model, and a Product model. The _Ecommerce_ App will allow users to signup/signin and add, remove, edit items to the shopping cart. A user will be able to view their recent order history. The super user will be able to create, edit, and remove products from the admin panel. A super user will also be able to edit and remove users from the admin panel.
> 
> ## Catalogue of Routes
>> ### Auth Routes
>>> | HTTP Method | URL Path | Action | CRUD |
>>> |--|--|--|--|
>>> | POST | /sign-up | create | (C)reate |
>>> | POST | /sign-in | create | (C)reate |
>>> | DELETE | /sign-out | destroy | (D)elete |
>>> | PATCH | /change-password | update | (U)pdate |
>>>
>> ###### [(Return to top)](https://github.com/EricHoward27/ecommerce-api#ecommerce-api)
>>
>> ### Order Routes 
>>> | HTTP Method | URL Path | Action | CRUD |
>>> |--|--|--|--|
>>> | POST | /orders | create order | (C)reate |
>>> | GET | /orders | index or list | (R)ead |
>>> | GET | /orders/:id | show or retrieve | (R)ead |
>>> | PATCH | /orders/:id | update | (U)pdate |
>>> | DELETE | /orders/:id | destroy | (D)elete |
>>>
>> ###### [(Return to top)](https://github.com/EricHoward27/ecommerce-api#ecommerce-api)
>>
>> ### Product Routes 
>>> | HTTP Method | URL Path | Action | CRUD |
>>> |--|--|--|--|
>>> | POST | /products | create products | (C)reate |
>>> | GET | /products | index or list | (R)ead |
>>> | GET | /products/:id | show or retrieve | (R)ead |
>>> | PATCH | /products/:id | update | (U)pdate |
>>> | DELETE | /products/:id | destroy | (D)elete |
>>>
>> ###### [(Return to top)](https://github.com/EricHoward27/ecommerce-api#ecommerce-api)
>>
> ## Entity Relationship Diagram
> ![ERD]('./docs/image/ecommerceerd.png')
>> ###### [(Return to top)](https://github.com/EricHoward27/ecommerce-api#ecommerce-api)
>>