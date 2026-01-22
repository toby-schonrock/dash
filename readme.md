### Project Description

This is an example **Dash** project using **Docker** and a **MongoDB** database to store data, featuring **Dash Mantine Components** for the UI. It utilizes this [Gapminder dataset](https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv).

The application provides a web interface where users can visualize database records on a graph, with support for selecting multiple countries and specific data metrics. It also implements **two simple CRUD operations**: 
1. Delete selected countries from the live database.
2. Reset the database by reloading the original data from the CSV.

**Live Demo:** [schonrocks.com/tobias/demo/dash/](https://schonrocks.com/tobias/demo/dash/)

![Siteimage](./images/site.png)

#### Technical Details: Routing & Callbacks
As shown in the callback graph below, the app uses **clientside callbacks** to sync inputs with the URL. This allows search queries to be shared between users via links and enables the use of browser forward/back buttons to navigate query history.

![CallbackGraphImage](./images/callbackGraph.png "Callback graph")

---

### Deployment Instructions

**Prerequisites:**
Only **Docker** and **Git** are required. For example, on a Debian/Ubuntu system, these can be installed with:
`sudo apt install docker.io docker-compose-v2 git`

**Setup Steps:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/toby-schonrock/dash.git
   cd dash
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the root directory and set your MongoDB credentials:
   ```env
   MONGO_ROOT_USER=YOUR_USERNAME
   MONGO_ROOT_PASSWORD=YOUR_PASSWORD
   ```
   *Optional configuration:*
   ```env
   APP_ENV=development      # default: production
   BASE_PATH=/demo/dashapp  # default: /
   ```

3. **Launch:**
   Run the following command to start the server and database:
   ```bash
   sudo docker compose up --build
   ```
   *Note: Add `-d` to run in detached mode.* 
   The app will be accessible at: `http://127.0.0.1:8050{YOUR_BASE_PATH}`