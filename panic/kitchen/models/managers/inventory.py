"""Inventory Transaction model managers."""

from django.db import models

from ...exceptions import ProcessingError


class InventoryTransactionManager(models.Manager):
  """Update the inventory based on transaction events."""

  def adjustment(self, transaction):
    """Adjust a related item's inventory based on the transaction's quantity."""
    if transaction.quantity > 0:
      self.__credit_inventory(transaction)
    else:
      self.__debit_inventory(transaction)

  def __credit_inventory(self, transaction):
    super().get_queryset().create(
        transaction=transaction,
        item=transaction.item,
        remaining=transaction.quantity
    )

  def __debit_inventory(self, transaction):
    remaining = abs(transaction.quantity)
    inventory = self.__select_inventory_by_item(transaction.item)
    for record in inventory:
      if record.remaining <= remaining:
        remaining = self.__debit_full_record(record, remaining)
      else:
        remaining = self.__debit_partial_record(record, remaining)
      if remaining < 1:
        return

    self.__adjustment_error(transaction)

  def __select_inventory_by_item(self, item):
    return super().get_queryset().\
        filter(item=item).\
        order_by("transaction__datetime")

  @staticmethod
  def __debit_full_record(record, remaining):
    remaining -= record.remaining
    record.delete()
    return remaining

  @staticmethod
  def __debit_partial_record(record, remaining):
    record_starting_value = record.remaining
    record.remaining -= remaining
    record.save()
    remaining -= (record_starting_value - record.remaining)
    return remaining

  @staticmethod
  def __adjustment_error(transaction):
    error_message = (
        f"could not adjust inventory for transaction={transaction.id}, "
        f"item={transaction.item.id}, "
        f"transaction.quantity={transaction.quantity}, "
        f"item.quantity={transaction.item.quantity}"
    )
    raise ProcessingError(detail=error_message)
