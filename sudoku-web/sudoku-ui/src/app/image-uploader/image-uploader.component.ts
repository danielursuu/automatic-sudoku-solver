import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { ImageUploadService } from '../services/image-upload.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-image-uploader',
  templateUrl: './image-uploader.component.html',
  styleUrls: ['./image-uploader.component.css']
})
export class ImageUploaderComponent implements OnInit {

  constructor(
    private readonly imageUploadService: ImageUploadService,
    private readonly router: Router
  ) { }

  ngOnInit(): void {
  }

  onUploadHandler(event, fileUpload) {
    this.imageUploadService.uploadImage(event.files[0]).subscribe(
      (response) => {
        console.log(response);
        this.router.navigate(['/validator']);
      },
      (error) => console.log(error)
    );
    fileUpload.clear();
  }

}
