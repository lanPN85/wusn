from wusn.propose.python_datastructure.single_link_list import SingleLinkList


class Queue(SingleLinkList):
    def enqueue(self, data):
        return self.insert_at_current(data)

    def de_queue(self):
        return self.delete_at_root()


#
# queue = Queue();
# queue.enqueue(5);
# queue.enqueue(6);
# queue.enqueue("Hello world");
# print(queue);
# queue.de_queue();
# print(queue);
# queue.de_queue();
# print(queue);