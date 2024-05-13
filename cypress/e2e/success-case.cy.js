
describe('Success case', () => {

  it('Test1', () => {

    // Navigating to the checkout page
    cy.visit('http://localhost:8080/home')
    cy.contains('Explore books').click() // Clicking to see the list of books
    cy.contains('View Details').click() // Clicking to see one book details
    cy.contains('Checkout').click() // Starting the checkout for that book

    // Entering the inouts for the checkout
    cy.get('input[name="userName"]').type('Mari Tamm')
    cy.get('input[name="userContact"]').type('maritamm@meil.com')

    cy.get('input[name="billingAddressStreet"]').type('Riia')
    cy.get('input[name="billingAddressCity"]').type('Tartu')
    cy.get('input[name="billingAddressState"]').type('Tartumaa')
    cy.get('input[name="billingAddressZip"]').type('50505')
    cy.get('select[name="billingAddressCountry"]').select('Estonia')

    cy.get('input[name="creditCardNumber"]').type('1234567890')
    cy.get('input[name="creditCardExpirationDate"]').type('10/26')
    cy.get('input[name="creditCardCVV"]').type('8275')

    cy.get('input[name="termsAndConditionsAccepted"]').click()

    // Submitting the order
    cy.contains('Submit').click()

    // Checking the result
    cy.contains("Order Approved")
    cy.contains("Suggested Books")

  })

})