# django_backoffice
This is an example project of implementing business processes within a company's backoffice.

# Architecture
This application can be installed on a `classical virtualenv` or on a `docker-compose structure`.

I recommend the installation of `docker-compose structure` because it's very easy and bultin and the app will need for this services:
- **django** (webapp: the host web product in `python`)
- **postgres** (database: to store the app data)
- **celery** (worker: to execute asynchronous tasks)
- **rabbitmq** (message broker: to delivery asynchronous tasks from webapp to worker)
- **nginx** (static files: to serve css, js and image files)

### Installing by docker-compose
#### Requirements:
- **docker engine** (on your OS): If you need to install (docker engine) [[please read the official documentation]](https://docs.docker.com/engine/install/)
- **docker-compose** (command): If you need to install (docker-compose tool) [[please read the official documentation]](https://docs.docker.com/engine/install/)
- **git** (command): If you need to install (git command) [[please read the official documentation]](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Execute the commands
**1.) Getting this repository**
```sh
git clone https://github.com/samukasmk/django_backoffice.git
```

**2.) Creating containers**
```sh
cd django_backoffice
docker-compose up
```
- Execute commands above to create all containers
- Waits until the end of the process (it's important) 
- Let this command running in current terminal tab
- Open another terminal tab to execute the next command (without stopping this)

![](.docs/images/1-creating-containers.png)

> Note: on the first time it will be very slow for downloading images.

**3.) Creating initial database values**
```sh
docker-compose exec django make install
```
This automatic step will:
- Import initial value on db (from json files)
- Create first super admin (and password)
- Create static files to be served on nginx

![](.docs/images/2-make-install.png)

> Note: After execute this command it'll prompt an information asking for (superadmin) user and password, please type it when asked on command line output.

## Accessing the application
- Open in you browser the url: [http://127.0.0.1/admin](http://127.0.0.1/admin)

![](.docs/images/3-login-page.png)

- Enter your superadmin username and password
- Use the app! 🎉

![](.docs/images/4-menu.png)

## Screenshots
### Customers
Creating a customer:
![](.docs/images/5-customer-create.png)

---

Listing customers:
![](.docs/images/6-customer-list.png)

# Products
Creating a product:
![](.docs/images/7-product-create.png)

---

Listing products:
![](.docs/images/8-product-list.png)

---

Creating products type (assigning on pipelines business process):
![](.docs/images/9-product-type-list.png)

---

# Business process pipelines
Listing business process pipelines:
![](.docs/images/10-pipeline-list.png)

---

Listing business process tasks:
![](.docs/images/11-pipeline-task.png)

---

Defining custom task arguments:
![](.docs/images/12-task-arguments.png)

---

Declaring custom task on code:
![](.docs/images/code-1-creating-custom-task.png)

---

Enabling custom task to run from db: 
![](.docs/images/code-2-allowing-custom-task.png)


# Salespeople
Creating a seller:
![](.docs/images/13-seller-create.png)

---

Listing sellers:
![](.docs/images/14-seller-list.png)

# Orders
Creating an Order:
![](.docs/images/15-order-create.png)

---

Listing created Orders:
![](.docs/images/16-order-list.png)

---

Executing actions on specific Order:
![](.docs/images/17-order-actions.png)

---

# Packing Slips
Accessing Packing Slip details on icon button:
![](.docs/images/18-packing-slip-details-button.png)

---

Viewing Packing Slip details on screen:
![](.docs/images/19-packing-slip-details-view.png)

---

Printing Packing Slip PDF file:
![](.docs/images/20-packing-slip-details-print-pdf.png)

---

Viewing Packing Slip PDF file:
![](.docs/images/21-packing-slip-details-view-pdf.png)

---

# Payments
Approving or Reproving Seller commissions payments:
![](.docs/images/22-seller-commission-list.png)

---

Approving or Reproving Roaylties payments:
![](.docs/images/23-royalties-payment-list.png)

---

# Monitoring of business process tasks
Observing when business process tasks were performed: 
![](.docs/images/25-monitoring-full-list.png)

