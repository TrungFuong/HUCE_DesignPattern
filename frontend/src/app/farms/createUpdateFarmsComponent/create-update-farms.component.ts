import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../auth.service';
import { User } from '../../users/user.model';
import { Farm, FarmPayload } from '../farm.model';

@Component({
  selector: 'app-create-update-farms',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './create-update-farms.component.html',
  styleUrls: ['./create-update-farms.component.scss'],
})
export class CreateUpdateFarmsComponent implements OnChanges, OnInit {
  private readonly usersService = inject(UsersService);
  private readonly authService = inject(AuthService);

  @Input() farm: Farm | null = null;
  @Input() farmers: User[] = [];
  @Input() ownerLocked = false;
  @Input() farmersError = '';
  @Input() isLoadingFarmers = false;
  @Input() isSaving = false;
  @Output() cancel = new EventEmitter<void>();
  @Output() save = new EventEmitter<FarmPayload>();

  form: FarmPayload = this.createEmptyForm();

  get title(): string {
    return this.farm ? 'Cập nhật thông tin nông trại' : 'Tạo mới nông trại';
  }

  get isFarmer(): boolean {
    return this.authService.getRole() === 1;
  }

  ngOnInit(): void {
    this.loadFarmers();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['farm'] || changes['farmers'] || changes['ownerLocked']) {
      this.form = this.farm
        ? {
            owner_id: this.farm.owner_id,
            name: this.farm.name,
            address: this.farm.address,
            planting_date: this.toDateInputValue(this.farm.planting_date),
            harvest_date: this.toDateInputValue(this.farm.harvest_date),
          }
        : {
            ...this.createEmptyForm(),
            owner_id: this.ownerLocked && this.farmers.length ? this.farmers[0].id : '',
          };
    }
  }

  submit(): void {
    if (this.isSaving) {
      return;
    }
    this.save.emit({
      ...this.form,
      planting_date: this.form.planting_date || null,
      harvest_date: this.form.harvest_date || null,
    });
  }

  private loadFarmers(): void {
    this.isLoadingFarmers = true;
    this.farmersError = '';

    const currentUser = this.authService.getCurrentUser();
    if (this.isFarmer && currentUser) {
      this.farmers = [currentUser];
      this.form = {
        ...this.form,
        owner_id: currentUser.id,
      };
      this.isLoadingFarmers = false;
      return;
    }

    this.usersService.getFarmers().subscribe({
      next: (farmers) => {
        this.farmers = farmers.filter((farmer) => farmer.is_active);
        this.isLoadingFarmers = false;
      },
      error: (error: HttpErrorResponse) => {
        const detail = error.error?.detail;
        this.farmersError =
          typeof detail === 'string'
            ? detail
            : 'Không thể tải danh sách nông dân từ hệ thống.';
        this.isLoadingFarmers = false;
      },
    });
  }

  private createEmptyForm(): FarmPayload {
    return {
      owner_id: '',
      name: '',
      address: '',
      planting_date: null,
      harvest_date: null,
    };
  }

  private toDateInputValue(value: string | null): string | null {
    return value ? value.slice(0, 10) : null;
  }
}
