from wusn.propose.python_datastructure.single_link_list import SingleLinkList


class Stack(SingleLinkList):
    def push(self, data):
        return self.insert_at_root(data);

    def pop(self):
        return self.delete_at_root()


# print("Stack");
# stack = Stack();
# result = stack.is_empty();
# print(result);
# stack.push(5);
# stack.push(6);
# stack.push(7);
# stack.push(8);
# stack.push("Hello world");
# stack.push("data ");
# print(stack);
# stack.pop();
# print(stack);
# stack.pop();
# print(stack);
# stack.pop();
# print(stack);
# result = stack.is_empty();
# print(result);