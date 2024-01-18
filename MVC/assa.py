                # # Game Page
                # if self.model.currentstate == 3:
                #     self.model.screen.blit(self.model.img, (0, 0))
                #     self.model.Mediapipe_pose_class.draw_shoulder_line (self.model.img)
                    
                #     # self.model.Mediapipe_pose_class.draw_all_landmark_line(self.model.img)
                    
                #     font = cv2.FONT_HERSHEY_SIMPLEX
                #     font_scale = 1
                #     font_thickness = 2
                #     font_color = (255, 255, 255)  # 白色       
                #     box_color = (0, 0, 255)  # 红色     
                #     self.model.time_left  = 3 - self.model.elapsed_time

                #     # display the count down
                #     box_position = (400, 50)
                #     box_size = (100, 100)
                #     cv2.rectangle(self.model.img, box_position, (box_position[0] + box_size[0], box_position[1] + box_size[1]), box_color, -1)
                #     text_position = (box_position[0] + 25, box_position[1] + box_size[1] // 2)
                #     cv2.putText(self.model.img, "{:.0f}".format(self.model.time_left), text_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

                
                #     # display the score
                #     text3 = "Score:{}  ".format(self.model.total_score)
                #     text3 = text3+("Missed" if self.model.hit_goal == False else "Hit")
                #     box_size = (300,100)
                #     box_position = (900,400)
                #     text3_position = (box_position[0] + 50, box_position[1] + box_size[1] // 2)
                #     cv2.rectangle(self.model.img, box_position, (box_position[0] + box_size[0], box_position[1] + box_size[1]), box_color, -1)
                #     cv2.putText(self.model.img, text3, text3_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)
                    
                #     # display the twist direction hint
                #     text2 = "please twist {}".format(self.model.Mediapipe_pose_class.direction)
                #     box_size = (500,100 )
                #     box_position = (900, 50)
                #     text2_position = (box_position[0] + 50, box_position[1] + box_size1] // 2)
                #     cv2.rectangle(self.model.img, box_position, (box_position[0] + box_size[0], box_position[1] + box_size[1]), box_color, -1)
                #     cv2.putText(self.model.img, text2, text2_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

                #     # progress bar
                #     white = (255, 255, 255)
                #     green = (0, 255, 0)
                #     level = self.model.Mediapipe_pose_class.max_level
                #     pygame.draw.rect(self.model.screen, green, (50, 50, 100*level, 50))
                #     if 0 <self.model.elapsed_time -3 < 1:
                #         self.model.Mediapipe_pose_class.max_level_store = 0