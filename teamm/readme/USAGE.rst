IMPORT ROOMS
models:
    resource.group (optional)
    resource.resource
    resource.booking.combination
    resource.booking.type
    resource.booking.type.combination.rel
aliases:
    resource.resource: resource.group
columns:
    resource.group
    room size
    resource.booking.type


IMPORT PRODUCT ATTRIBUTES
models:
    product.attribute
    product.attribute.value
aliases:
    product.attribute.value: resource.booking.type
columns:
    product.attribute
    create variant (optional)
    product.attribute.value

product.template

sale.order
sale.order.line
resource.booking


EXTERNAL API INTEGRATION

res.partner
resource.booking.type
resource.resource
resource.booking.combination
resource.booking.type.combination.rel
product.attribute.value
product.template
product.template.attribute.line
product.product
sale.order
sale.order.line
resource.booking
payment.link.wizard

DEMO.XML

resource.calendar
resource.calendar.attendance

resource.resource (sessions and rooms)
# res.users
# resource.resource (users)
# hr.employee
resource.booking.combination
resource.booking.type
resource.booking.type.combination.rel
resource.booking
product.public.category
product.product
product.attribute
product.attribute.value

product.template
product.template.attribute.line
ir.model.data
product.template.attribute.value
ir.model.data
product.pack.line

resource.booking (periods)
product.pricelist
product.pricelist.item
res.partner
ir.property
payment.provider
