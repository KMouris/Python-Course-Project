class CheckInputData:
    def __init__(self, array_one, array_two):
        self.array_one
        self.array_two

    def compare_shape(self, array_one, array_two):
        if not array_one.shape == array_two.shape:
            if not array_one.shape[0] == array_two.shape[0]:
                print("Unequal number of rows.")
            else:
                print("Unequal number of columns.")
        # else:
            # print("Arrays have the same shape.")

    def number_of_items(self, object_one, object_two):
        if not len(object_one) == len(object_two):
            if len(object_one) < len(object_two):
                print("More items in object_two.")
            else:
                print("More items in object_one.")
        # else:
            # print("Same number of items.")


