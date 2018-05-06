import numpy as np

class Life(object):
    def __init__(self):
        self.static = False
        self.n_step = 0
        self.color = np.array(np.random.rand(3) * 127.0, dtype=np.uint8)
        self.state = np.zeros((17, 17), dtype=bool)
        self.state[(np.random.rand(17, 17) < 0.1)] = True
        self.state[10:12, 10:12] = True

        self.old_state = np.array(self.state)

    def is_extinct(self):
        return not self.state.any()

    def step(self):
        next_state = np.zeros(self.state.shape, dtype=bool)
        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                # neighbors
                cnt = 0
                for a in [-1, 0, 1]:
                    for b in [-1, 0, 1]:
                        if a == 0 and b == 0:
                            continue

                        if self.state[(i + a) % self.state.shape[0], (j + b) % self.state.shape[1]]:
                            cnt += 1

                if self.state[i,j]:
                    #print("({},{}) : {}".format(i, j, cnt))
                    if cnt < 2:
                        next_state[i,j] = False
                    elif cnt > 3:
                        next_state[i,j] = False
                    else:
                        next_state[i,j] = True
                else:
                    if cnt == 3:
                        next_state[i,j] = True

        if (self.state == next_state).all():
            self.static = True

        self.old_state = np.array(self.state)
        self.state = next_state
        self.n_step += 1
                        
    def render(self):
        img = np.zeros((17, 17, 3), dtype=np.uint8)
        img[self.state,:] = self.color
        return img

    def render_transition(self, frac):
        img = np.zeros((17, 17, 3), dtype=np.uint8)
        img[self.state,:] += np.array(np.clip(np.floor(frac * self.color), 0, 255), dtype=np.uint8)
        img[self.old_state,:] += np.array(np.clip(np.floor((1.0 - frac) * self.color), 0, 255), dtype=np.uint8)
        return img

