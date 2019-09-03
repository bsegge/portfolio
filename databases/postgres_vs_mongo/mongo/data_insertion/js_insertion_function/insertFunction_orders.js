add_order = function (first_name, last_name, recipe) {
    // set user variable, inserting if not found
    db.users.update({name: first_name, last_name: last_name}, {
        "first_name": first_name,
        "last_name": last_name
    }, {upsert: true})
    var user = db.users.findOne({"first_name": first_name, "last_name": last_name})
    // set recipe variable
    var recipe = db.recipes.findOne({"name": recipe})
    // set recipe name variable (unneeded, but helpful)
    var recipe_name = recipe.name

    // find the ingredients needed for given recipe
    db.recipes.find({name: recipe_name}, {_id: 1, ingredients: 1}).forEach(function (doc) {
        var ing = doc.ingredients
        for (var idx = 0; idx < ing.length; idx++) {
            // set inventory amount
            var inv_amt = db.inventory.findOne({name: ing[idx].name}).quantity
            // check that we have enough inventory and if so,
            // decrement recipe ingredient quantity from inventory
            if (ing[idx].qty > inv_amt) throw "not enough"
            db.inventory.update({name: ing[idx].name}, {$inc: {quantity: -ing[idx].qty}})
        }
    })
    // insert order
    db.orders.insert({
        "first_name": user.first_name,
        "last_name": user.last_name,
        "timestamp": new Date(),
        "recipe": recipe_name
    })
}
