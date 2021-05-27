# This is a sample Python script.
import lerInst as li

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

if __name__ == '__main__':

    n,adj,req,g = li.lerTXT('brasil.txt')
    print(g.number_of_nodes())
    print(g.nodes())
    print(g.edges())