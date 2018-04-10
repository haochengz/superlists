
from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.saving_list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.saving_list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first = saved_items[0]
        second = saved_items[1]
        self.assertEqual(first.text, first_item.text)
        self.assertEqual(first.saving_list, list_)
        self.assertEqual(second.text, second_item.text)
        self.assertEqual(second.saving_list, list_)

    def test_cannot_save_empty_items(self):
        list_ = List.objects.create()
        item_ = Item(saving_list=list_, text="")
        with self.assertRaises(ValidationError):
            item_.save()
            item_.full_clean()


