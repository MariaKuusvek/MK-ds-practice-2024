

describe('Success case', () => {

  it('Navigating to checkout page', () => {
    cy.visit('http://localhost:8080/home')

    cy.contains('Explore books').click()

    cy.contains('View Details').click()

    cy.contains('Checkout').click()

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

    cy.contains('Submit').click()

    cy.contains("Order Approved")

  })

})