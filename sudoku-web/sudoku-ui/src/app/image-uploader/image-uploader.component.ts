import { Component, OnInit, Output, EventEmitter } from '@angular/core';

import { ImageUploadService } from '../services/image-upload.service';

@Component({
  selector: 'app-image-uploader',
  templateUrl: './image-uploader.component.html',
  styleUrls: ['./image-uploader.component.css']
})
export class ImageUploaderComponent implements OnInit {

  @Output()
  uploaded = new EventEmitter<any>();

  constructor(
    private readonly imageUploadService: ImageUploadService
  ) { }

  ngOnInit(): void {
  }

  onUploadHandler(event, fileUpload) {
    this.imageUploadService.uploadImage(event.files[0]).subscribe(
      (response) => {
        this.uploaded.emit(response);
      },
      (error) => console.log(error)
    );
    fileUpload.clear();
  }

}
