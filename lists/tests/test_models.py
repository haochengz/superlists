
from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ItemModelTest(TestCase):

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

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.saving_list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())


    def test_cannot_save_empty_items(self):
        list_ = List.objects.create()
        item_ = Item(saving_list=list_, text="")
        with self.assertRaises(ValidationError):
            item_.save()
            item_.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(saving_list=list_, text="bla")
        with self.assertRaises(ValidationError):
            item_ = Item(saving_list=list_, text="bla")
            item_.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(saving_list=list1, text="bla")
        item_ = Item(saving_list=list2, text="bla")
        item_.full_clean()

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(saving_list=list1, text='i1')
        item2 = Item.objects.create(saving_list=list1, text='i2')
        item3 = Item.objects.create(saving_list=list1, text='i3')

        self.assertEqual(
                list(Item.objects.all()),
                [item1, item2, item3]
            )


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        pass
