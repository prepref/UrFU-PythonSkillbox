class dynamic_array:
    data = []
    capacity = 0
    length = 0

    def __init__(self, n) -> None:
        self.data = [0] * n
        self.capacity = n
    
    def push(self, n):
        if self.length >= self.capacity:
            new_capacity = self.capacity * 2
            new_data = [0] * new_capacity
            j = 0
            for i in self.data:
                new_data[j] = i
                j+=1
            self.data = new_data
            self.capacity = new_capacity
        
        self.data[self.length] = n
        self.length += 1
    
    def pop(self):
        if (self.capacity - self.length) // 3 >= self.length:
            new_capacity = self.capacity//2
            new_data = [0] * new_capacity
            j = 0
            for i in self.data:
                new_data[j] = i
                j += 1
            self.data = new_data
            self.capacity = new_capacity
        
        self.data[self.length] = 0
        self.length -= 1

    def get(self, n):
        return self.data.index(n)
    
    def set(self, n, val):
        self.data.insert(n,val)
    
    def get_length(self):
        return self.length
    
    def get_capacity(self):
        return self.capacity