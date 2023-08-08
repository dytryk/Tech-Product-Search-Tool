/**
Author: Dietrich Sinkevitch
Program: Tech Product Search Tool
Date: 08/08/2023
Github Link: https://github.com/dytryk/techproductsearchtool
 */

function deleteProduct(product_id) {
  /**
   * This function sends a request to delete a product from the database.
   * it is called by 'products.html' and interacts with 'views.delete_product'
   */
  fetch("/delete-product", {
    method: "POST",
    body: JSON.stringify({ id: product_id }),
  }).then((_res) => {
    window.location.href = "/products";
  });
}

function selectProduct(product_id) {
  /**
   * This function sends a request to change the value of the select attribute for a priduct from 0 to 1.
   * the selected products are those which the user wants to recieve notifications about.
   * this function is called by 'products.html' and interacts with 'views.select_product'
   */
  fetch("/select-product", {
    method: "POST",
    body: JSON.stringify({ id: product_id }),
  }).then((_res) => {
    window.location.href = "/products";
  });
}

/**
 * The path to this file is defined in the 'base_auth.html' file.
 */