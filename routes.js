const express = require('express');
const Joi = require('joi');
const Product = require('../models/Product');
const router = express.Router();

// validación con Joi
const productSchema = Joi.object({
  name: Joi.string().min(1).required(),
  price: Joi.number().min(0).required(),
  stock: Joi.number().integer().min(0).optional(),
  description: Joi.string().optional().allow('')
});

// CREATE
router.post('/', async (req, res, next) => {
  try {
    const { error, value } = productSchema.validate(req.body);
    if (error) return res.status(400).json({ error: error.message });

    const prod = new Product(value);
    await prod.save();
    res.status(201).json(prod);
  } catch (err) { next(err); }
});

// READ (listado con paginación y filtros simples)
router.get('/', async (req, res, next) => {
  try {
    const { page = 1, limit = 10, q } = req.query;
    const filter = q ? { name: new RegExp(q, 'i') } : {};
    const skip = (Math.max(1, parseInt(page)) - 1) * parseInt(limit);
    const [items, total] = await Promise.all([
      Product.find(filter).skip(skip).limit(parseInt(limit)).exec(),
      Product.countDocuments(filter)
    ]);
    res.json({ page: parseInt(page), limit: parseInt(limit), total, items });
  } catch (err) { next(err); }
});

// READ one
router.get('/:id', async (req, res, next) => {
  try {
    const prod = await Product.findById(req.params.id);
    if (!prod) return res.status(404).json({ error: 'Producto no encontrado' });
    res.json(prod);
  } catch (err) { next(err); }
});

// UPDATE (PUT - reemplazo)
router.put('/:id', async (req, res, next) => {
  try {
    const { error, value } = productSchema.validate(req.body);
    if (error) return res.status(400).json({ error: error.message });
    const prod = await Product.findByIdAndUpdate(req.params.id, value, { new: true, runValidators: true });
    if (!prod) return res.status(404).json({ error: 'Producto no encontrado' });
    res.json(prod);
  } catch (err) { next(err); }
});

// PATCH (actualización parcial)
router.patch('/:id', async (req, res, next) => {
  try {
    const allowed = ['name','price','stock','description'];
    const updates = {};
    for (const k of allowed) if (k in req.body) updates[k] = req.body[k];
    const prod = await Product.findByIdAndUpdate(req.params.id, updates, { new: true, runValidators: true });
    if (!prod) return res.status(404).json({ error: 'Producto no encontrado' });
    res.json(prod);
  } catch (err) { next(err); }
});

// DELETE
router.delete('/:id', async (req, res, next) => {
  try {
    const prod = await Product.findByIdAndDelete(req.params.id);
    if (!prod) return res.status(404).json({ error: 'Producto no encontrado' });
    res.status(204).send();
  } catch (err) { next(err); }
});

module.exports = router;
 